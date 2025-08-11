from fpdf import FPDF
import datetime
import os
from app.analyzer import parse_markdown  # importer la fonction markdown

class PDF(FPDF):
    def write_markdown_line(self, parsed_line):
        if len(parsed_line) == 1 and parsed_line[0][1].startswith("title_"):
            title, style = parsed_line[0]
            level = int(style.split("_")[1])
            if level == 1:
                self.set_font("DejaVu", "B", 18)
                self.set_text_color(0, 0, 80)  # Bleu foncé
            elif level == 2:
                self.set_font("DejaVu", "B", 14)
                self.set_text_color(20, 20, 20)
            elif level == 3:
                self.set_font("DejaVu", "B", 12)
                self.set_text_color(50, 50, 50)
            else:
                self.set_font("DejaVu", "", 12)
                self.set_text_color(0, 0, 0)

            self.cell(0, 10, title, ln=True)
            self.ln(2)
        else:
            self.set_text_color(0, 0, 0)  # Texte normal en noir
            for text, style in parsed_line:
                if style == "bold":
                    self.set_font("DejaVu", "B", 12)
                elif style == "italic":
                    self.set_font("DejaVu", "I", 12)
                else:
                    self.set_font("DejaVu", "", 12)
                self.write(6, text)
            self.ln(8)

def generate_pdf_report(summary_text):
    # Génère un nom de fichier avec la date/heure
    path = f"rapport_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    pdf = PDF()
    pdf.add_page()

    # Chemin vers la police Unicode
    font_path = os.path.join("fonts", "DejaVuSans.ttf")
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Police Unicode manquante : {font_path}")

    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.add_font("DejaVu", "B", font_path, uni=True)
    pdf.add_font("DejaVu", "I", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    # Titre
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 10, "Rapport Financier généré par IA", ln=True)
    pdf.ln(5)

    # Ajout du graphique utilisateur s'il existe
    graph_path = os.path.join("app", "graphique_utilisateur.png")
    if os.path.exists(graph_path):
        try:
            pdf.set_font("DejaVu", "B", 12)
            pdf.cell(0, 10, "Graphique généré à partir des données utilisateur :", ln=True)
            pdf.ln(2)
            # Largeur max = 170mm, hauteur max = 100mm
            pdf.image(graph_path, w=170, h=100)
            pdf.ln(8)
        except Exception as e:
            pdf.set_font("DejaVu", "", 10)
            pdf.cell(0, 10, f"Erreur lors de l'insertion du graphique : {e}", ln=True)
            pdf.ln(5)

    # Contenu : traite chaque ligne en Markdown
    for line in summary_text.split("\n"):
        if not line.strip():
            pdf.ln(5)
            continue
        parsed = parse_markdown(line)
        pdf.write_markdown_line(parsed)

    pdf.output(path)
    return path