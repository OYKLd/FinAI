import streamlit as st
from services.api_client import send_file_for_report
from components import upload, charts

st.set_page_config(page_title="Générateur de Rapport Financier", layout="centered")
st.title("📊 Générateur Intelligent de Rapport Financier")

# Chargement du fichier
uploaded_file = upload.upload_financial_file()

if uploaded_file:
    with st.spinner("Analyse et génération du rapport..."):
        # Envoyer au backend
        response = send_file_for_report(uploaded_file)

        if response.ok:
            st.success("✅ Rapport généré avec succès !")
            st.download_button(
                label="📥 Télécharger le rapport PDF",
                data=response.content,
                file_name="rapport_financier.pdf",
                mime="application/pdf"
            )
        else:
            st.error("❌ Erreur lors de la génération du rapport. Veuillez réessayer.")