from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def generate_pdf(data):

    doc = SimpleDocTemplate("medical_report.pdf")
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("AI Brain Hemorrhage Medical Report", styles['Title']))
    elements.append(Spacer(1, 0.5 * inch))

    elements.append(Paragraph(f"Diagnosis: {data['diagnosis']}", styles['Normal']))
    elements.append(Paragraph(f"Confidence: {data['confidence']:.2f}", styles['Normal']))
    elements.append(Paragraph(f"Severity: {data['severity']}", styles['Normal']))
    elements.append(Paragraph(f"Location: {data['location']}", styles['Normal']))
    elements.append(Paragraph(f"Symptoms: {data['symptoms']}", styles['Normal']))
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("AI Advice:", styles['Heading2']))
    elements.append(Paragraph(data['advice'], styles['Normal']))

    doc.build(elements)