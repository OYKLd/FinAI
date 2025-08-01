FinAI/
├── app/
│   ├── api/
│   │   └── fastapi_app.py           # API FastAPI
│   ├── extractor/
│   │   ├── base.py                  # Interface d'extraction
│   │   ├── pdf.py                   # PDF
│   │   ├── excel.py                 # Excel
│   │   ├── word.py                  # Word
│   │   └── ocr.py                   # OCR image
│   ├── analyzer/
│   │   └── gpt_analyzer.py          # Résumé IA avec GPT-4
│   ├── report/
│   │   └── pdf_report.py            # Génération de rapport PDF
├── requirements.txt
└── README.md
