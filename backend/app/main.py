from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import report

app = FastAPI(
    title="Générateur de Rapport Financier",
    description="API pour générer automatiquement des rapports financiers à partir de fichiers Excel ou CSV.",
    version="1.0.0"
)

# Autoriser le frontend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes
app.include_router(report.router)