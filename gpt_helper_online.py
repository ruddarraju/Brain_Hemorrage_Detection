from groq import Groq

client = Groq(api_key="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")

SYSTEM_PROMPT = """
You are a professional AI Neurology Assistant.
Provide structured medical guidance.
Be clear and concise.
Always include disclaimer.
"""

def generate_chat_reply(diagnosis, location, symptoms, probability, severity):

    user_prompt = f"""
Diagnosis: {diagnosis}
Confidence Score: {probability:.2f}
Severity: {severity}
Location: {location}
Symptoms: {symptoms}

Provide:
1. Explanation
2. Emergency warning signs
3. Immediate precautions
4. Doctor consultation advice
Include disclaimer.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        print("Groq Error:", e)
        return "AI service temporarily unavailable."