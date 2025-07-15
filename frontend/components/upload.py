import streamlit as st

def upload_financial_file():
    st.subheader("📂 Importer vos données financières")
    file = st.file_uploader("Sélectionnez un fichier CSV ou Excel", type=["csv", "xls", "xlsx"])
    if file:
        st.info(f"Fichier importé : **{file.name}**")
    return file