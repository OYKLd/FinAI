# app/main.py
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.extractor import extract_data
from app.analyzer import analyze_data
from app.report_generator import generate_pdf_report

load_dotenv()
app = FastAPI(title="FinAI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze/")
async def analyze_files(files: list[UploadFile] = File(...)):
    contents = await extract_data(files)
    summary = analyze_data(contents)
    report_path = generate_pdf_report(summary)
    return FileResponse(report_path, filename="rapport_financier.pdf", media_type="application/pdf")

@app.get("/")
def root():
    return JSONResponse({"message": "Bienvenue sur FinAI API"})