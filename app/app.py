from flask import Flask, request, send_file
from flask_cors import CORS
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "API Running"

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    data = request.json

    file_path = "/tmp/body_report.pdf"   # 🔴 VERY IMPORTANT (Render needs /tmp)

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>Body Composition Analysis</b>", styles["Title"]))
    elements.append(Paragraph("Saroj Fitness & Ayurveda<br/><br/>", styles["Normal"]))

    table_data = [
        ["Weight", data["weight"], "BMI", data["bmi"]],
        ["Fat %", "23.06 High", "Muscle Mass", "54.93 Normal"],
        ["Skeletal Muscle", "31.22 Low", "Bone Mass", "2.89"],
        ["Hydration", "55.55%", "Visceral Fat", "7.17"],
        ["Protein", "17.54%", "BMR", "1618"]
    ]

    table = Table(table_data, colWidths=[120]*4)
    table.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),1,colors.grey),
        ('ALIGN',(0,0),(-1,-1),'CENTER')
    ]))

    elements.append(table)
    doc.build(elements)

    return send_file(
        file_path,
        as_attachment=True,
        download_name="Body_Composition_Report.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run()
