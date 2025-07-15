# FinAI

ai-financial-report-generator/
├── frontend/                              # Interface utilisateur (Streamlit)
│   ├── app.py                             # Application principale Streamlit
│   ├── components/                        # Composants personnalisés
│   │   ├── upload.py
│   │   └── charts.py
│   ├── services/                          # Appels vers API backend
│   │   └── api_client.py                  # Envoie les fichiers / requêtes à FastAPI
│   ├── assets/
│   │   ├── style.css
│   │   └── js/
│   │       └── charts.js
│   └── .streamlit/
│       └── config.toml
│
├── backend/                               # Backend avec FastAPI, LangChain, etc.
│   ├── app/
│   │   ├── main.py                        # Point d'entrée FastAPI
│   │   ├── routes/                        # Endpoints FastAPI
│   │   │   ├── report.py                  # Endpoint pour générer rapport
│   │   │   └── data.py                    # Endpoint pour analyse de données
│   │   ├── services/
│   │   │   ├── ai_generator.py            # Génération texte IA (OpenAI + LangChain)
│   │   │   ├── data_analysis.py           # Analyse (totaux, marges, etc.)
│   │   │   ├── pdf_service.py             # Création du rapport PDF
│   │   │   └── file_handler.py            # Upload et parsing fichiers
│   │   ├── core/
│   │   │   └── config.py                  # Paramètres FastAPI et OpenAI
│   │   └── models/
│   │       └── schemas.py                 # Pydantic Models (Input/Output)
│   └── requirements.txt
│
├── README.md
└── .env                                   # Clés API, etc. (non versionné)