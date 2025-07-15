from fpdf import FPDF
import tempfile

def create_pdf_report(text: str, insights: dict) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "Rapport Financier", ln=True, align="C")
    pdf.ln(10)

    pdf.multi_cell(0, 10, text)

    pdf.ln(10)
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(200, 10, "Résumé des chiffres :", ln=True)
    pdf.set_font("Arial", size=12)
    for key, value in insights.items():
        pdf.cell(200, 10, f"{key.capitalize()} : {value}", ln=True)

    path = tempfile.mktemp(suffix=".pdf")
    pdf.output(path)
    return path