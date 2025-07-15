from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from app.services import file_handler, data_analysis, ai_generator, pdf_service
import tempfile
import os

router = APIRouter()

@router.post("/generate-report", summary="Générer un rapport PDF à partir d'un fichier Excel ou CSV")
async def generate_report(file: UploadFile = File(...)):
    # Déterminer l'extension
    filename = file.filename
    ext = os.path.splitext(filename)[1]
    # Créer un fichier temporaire avec la bonne extension
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    # 1. Lecture des données
    df = file_handler.load_file(tmp_path)

    # 2. Analyse des données
    insights = data_analysis.analyze_financial_data(df)

    # 3. Génération du texte via IA
    report_text = ai_generator.generate_report_text(insights)

    # 4. Génération PDF
    pdf_path = pdf_service.create_pdf_report(report_text, insights)

    # Nettoyer le fichier temporaire
    os.remove(tmp_path)

    return FileResponse(pdf_path, filename="rapport_financier.pdf", media_type="application/pdf")