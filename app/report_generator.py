# app/report_generator.py

from fpdf import FPDF
import datetime
import os

def generate_pdf_report(summary_text):
    # Génère un nom de fichier avec la date/heure
    path = f"rapport_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    pdf = FPDF()
    pdf.add_page()

    # Chemin vers la police Unicode
    font_path = os.path.join("fonts", "DejaVuSans.ttf")
    
    # Vérifie que le fichier existe
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Police Unicode manquante : {font_path}")

    # Ajoute la police Unicode
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    # Titre
    pdf.multi_cell(0, 10, "Rapport Financier généré par IA", align="L")
    pdf.ln(5)

    # Contenu
    for line in summary_text.split("\n"):
        pdf.multi_cell(0, 10, line)

    # Sauvegarde du PDF
    pdf.output(path)
    return path
