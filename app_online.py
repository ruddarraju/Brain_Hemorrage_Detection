from flask import Flask, render_template, request, jsonify, session, send_file
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import requests
from gpt_helper_online import generate_chat_reply
from maps_helper import search_neurologists
from pdf_generator import generate_pdf

app = Flask(__name__)
app.secret_key = "brain_ai_online_secret"

model = load_model("densenet_bilstm_qio_model.h5", compile=False)
IMAGE_SIZE = 224


def preprocess_image(image):
    image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image


def predict_image(image):
    processed = preprocess_image(image)
    prediction = model.predict(processed)
    probability = float(prediction[0][0])
    diagnosis = "Hemorrhage" if probability > 0.5 else "Normal"
    return diagnosis, probability


def detect_location():
    try:
        res = requests.get("http://ip-api.com/json").json()
        return res.get("city")
    except:
        return "Unknown"


def calculate_severity(prob):
    if prob > 0.85:
        return "HIGH RISK"
    elif prob > 0.65:
        return "MODERATE RISK"
    else:
        return "LOW RISK"


@app.route("/")
def home():
    session.clear()
    return render_template("chat_online.html")


@app.route("/chat", methods=["POST"])
def chat():

    message = request.form.get("message")
    file = request.files.get("image")

    # CT Upload
    if file:
        image = Image.open(file).convert("RGB")
        diagnosis, prob = predict_image(image)
        severity = calculate_severity(prob)
        location = detect_location()

        session["diagnosis"] = diagnosis
        session["probability"] = prob
        session["severity"] = severity
        session["location"] = location

        if diagnosis == "Hemorrhage":
            return jsonify({
                "reply": f"""⚠️ Hemorrhage Detected
Confidence Score: {prob:.2f}
Severity Level: {severity}

📍 Detected Location: {location}

Please describe your symptoms."""
            })
        else:
            return jsonify({
                "reply": f"""✅ No Hemorrhage Detected
Confidence Score: {prob:.2f}
Severity Level: {severity}

Are you experiencing any symptoms?"""
            })

    # Symptoms message
    if message:
        diagnosis = session.get("diagnosis")
        location = session.get("location")
        probability = session.get("probability")
        severity = session.get("severity")

        doctors = search_neurologists(location) if location else []

        doctor_text = "\n".join(
            [f"- {doc['name']}" for doc in doctors]
        ) if doctors else "No doctors found."

        response = generate_chat_reply(
            diagnosis, location, message, probability, severity
        )

        full_response = response + f"\n\n🏥 Nearby Specialists:\n{doctor_text}"

        session["report_data"] = {
            "diagnosis": diagnosis,
            "confidence": probability,
            "severity": severity,
            "location": location,
            "symptoms": message,
            "advice": full_response
        }

        return jsonify({"reply": full_response})

    return jsonify({"reply": "Please upload a CT scan image first."})


@app.route("/download_report")
def download_report():
    data = session.get("report_data")

    if not data:
        return "Report not ready. Please complete AI consultation first."

    generate_pdf(data)
    return send_file("medical_report.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)