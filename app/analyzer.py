# app/analyzer.py
import os
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv  
load_dotenv()

prompt = PromptTemplate(
    input_variables=["data_str"],
    template="""
Tu es un expert financier et analyste comptable intelligent. Ton rôle est d’analyser un ou plusieurs documents financiers (factures, tableaux Excel, textes libres, relevés bancaires, etc.), quel que soit leur format (.pdf, .xlsx, .csv, .docx), pour en extraire automatiquement les données essentielles : montants, clients, dates, catégories de dépenses/recettes, périodes, etc.

Génére ensuite un rapport financier structuré, clair et professionnel en langage naturel en français, à destination de non-spécialistes. Ce rapport doit inclure :

Un résumé clair de la situation financière,

Une synthèse des revenus et des dépenses,

Une analyse des tendances ou des anomalies si possible,

Des recommandations ou observations.

Tous les montants doivent être affichés en FCFA (Francs CFA), avec clarté et lisibilité (ex : 1 500 000 FCFA).

Le rapport doit être organisé avec des titres, sous-titres, puces ou tableaux si nécessaire, et optimisé pour l’export en PDF.

Voici les fichiers à analyser : {data_str}
"""
)

llm = ChatOpenAI(
    model_name="gpt-4",
    openai_api_key=os.getenv("OPENAI_API_KEY")  
)
chain = LLMChain(llm=llm, prompt=prompt)

def analyze_data(content):
    all_text = []
    for item in content:
        if item["type"] == "table":
            all_text.append(item["data"].to_csv(index=False))
        elif item["type"] in ("text", "pdf"):
            all_text.append(item.get("text", ""))
    return chain.run(data_str="\n\n".join(all_text))