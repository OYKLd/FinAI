import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0.7)

def generate_report_text(insights: dict) -> str:
    prompt = f"""
    Rédige un rapport financier clair et professionnel basé sur les données suivantes :

    Résumé des finances :
    - Revenus totaux : {insights['revenus']}
    - Dépenses totales : {insights['depenses']}
    - Résultat net : {insights['net']}
    - Évolution mensuelle : {insights['evolution']} %

    Génère un texte structuré avec une introduction, une analyse des performances, et une conclusion.
    """

    messages = [HumanMessage(content=prompt)]
    return llm(messages).content