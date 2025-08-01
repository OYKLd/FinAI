# app/analyzer.py
import os
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import markdown
import re
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

def parse_markdown(text):
    """
    Analyse Markdown simple (titres, gras, italique) et retourne une liste de blocs formatés :
    - type = title / bold / italic / normal
    - level = 1, 2, 3 (pour les titres)
    """
    text = text.strip()
    
    # Traitement des titres
    match = re.match(r"^(#{1,6})\s+(.*)", text)
    if match:
        level = len(match.group(1))
        content = match.group(2)
        return [(content, f"title_{level}")]
    
    # Traitement du gras et italique
    parts = []
    pattern = re.compile(r"(\*\*(.*?)\*\*)|(\*(.*?)\*)")  # **bold** ou *italic*

    pos = 0
    for match in pattern.finditer(text):
        start, end = match.span()
        if start > pos:
            parts.append((text[pos:start], "normal"))
        if match.group(1):  # **bold**
            parts.append((match.group(2), "bold"))
        elif match.group(3):  # *italic*
            parts.append((match.group(4), "italic"))
        pos = end

    if pos < len(text):
        parts.append((text[pos:], "normal"))

    return parts


def analyze_data(content):
    """
    Prend les données extraites (texte+tables),
    les transforme en texte et génère un résumé GPT.
    """
    all_text = []
    for item in content:
        if "error" in item:
            all_text.append(f"Erreur lors du traitement du fichier : {item['error']}")
        elif item["type"] == "table":
            all_text.append(item["data"].to_csv(index=False))
        elif item["type"] in ("text", "pdf"):
            all_text.append(item.get("text", ""))

    data_str = "\n\n".join(all_text)
    raw_result = chain.run(data_str=data_str)
    
    return raw_result  # on garde le Markdown brut ici
