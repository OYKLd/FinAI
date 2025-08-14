import streamlit as st
import requests
import mimetypes
import pandas as pd
import matplotlib.pyplot as plt

# --- Configuration de la page ---
st.set_page_config(
    page_title="FinAI - Analyse Financière",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🌟 **FinAI - Analyse Financière** 🌟")

# --- Initialisation de l'historique ---
if "historique" not in st.session_state:
    st.session_state.historique = []

# --- Onglets ---
tabs = st.tabs(["📊 Graphiques", "📄 Rapport"])

# --- Onglet Graphiques ---
with tabs[0]:
    st.subheader("Importez vos données pour générer des graphiques")
    data_file = st.file_uploader(
        "Importer un fichier de données (CSV ou Excel)",
        type=["csv", "xlsx"],
        key="data_uploader"
    )

    df = None
    if data_file:
        try:
            # Lecture du fichier
            if data_file.name.endswith('.csv'):
                df = pd.read_csv(data_file)
            else:
                df = pd.read_excel(data_file)

            # Conversion des colonnes numériques
            for col in df.columns[1:]:
                df[col] = df[col].astype(str).str.replace(" ", "").str.replace("\u00A0", "").str.replace(",", ".")
                df[col] = pd.to_numeric(df[col], errors='coerce')

            st.success("✅ Données chargées avec succès !")
            st.dataframe(df)

            # Colonnes pour choix graphique / affichage
            col1, col2 = st.columns([1, 2])
            with col1:
                chart_type = st.selectbox("Type de graphique", ("Lignes", "Camembert"))

            with col2:
                if chart_type == "Lignes":
                    numeric_cols = df.select_dtypes(include='number').columns
                    if len(numeric_cols) > 0:
                        fig, ax = plt.subplots()
                        df[numeric_cols].plot(ax=ax)
                        st.pyplot(fig)
                        fig.savefig("app/graphique_utilisateur.png")
                    else:
                        st.warning("Aucune colonne numérique trouvée pour générer un graphique.")
                else:
                    if len(df.columns) > 1:
                        col = st.selectbox("Colonne pour le camembert", options=df.columns[1:])
                        fig, ax = plt.subplots()
                        ax.pie(df[col], labels=df[df.columns[0]], autopct='%1.1f%%', startangle=90)
                        ax.axis('equal')
                        st.pyplot(fig)
                        fig.savefig("app/graphique_utilisateur.png")
                    else:
                        st.warning("Impossible de générer un camembert : pas assez de colonnes.")

        except Exception as e:
            st.error(f"Erreur lors du chargement des données : {e}")

# --- Onglet Rapport ---
with tabs[1]:
    st.subheader("Générez votre rapport financier")
    uploaded_file = st.file_uploader(
        "Choisissez un fichier (PDF, Excel, CSV, Image)",
        type=["pdf", "csv", "xls", "xlsx", "png", "jpg", "jpeg"],
        key="rapport_uploader"
    )

    if uploaded_file:
        mime_type, _ = mimetypes.guess_type(uploaded_file.name)
        if mime_type is None:
            mime_type = "application/octet-stream"
        files = [("files", (uploaded_file.name, uploaded_file, mime_type))]

        with st.spinner("🌀 Analyse en cours..."):
            try:
                response = requests.post("http://localhost:8000/analyze/", files=files)
                if response.status_code == 200:
                    st.success("✅ Rapport généré avec succès !")
                    
                    # Sauvegarde dans l'historique
                    st.session_state.historique.append({
                        "nom": uploaded_file.name.replace(".", "_") + "_rapport.pdf",
                        "contenu": response.content
                    })

                    st.download_button(
                        "📥 Télécharger le rapport PDF",
                        data=response.content,
                        file_name="rapport_financier.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error(f"Erreur lors de la génération du rapport : {response.text}")
            except Exception as e:
                st.error(f"Connexion API impossible : {e}")

# --- Affichage de l'historique ---
if st.session_state.historique:
    st.subheader("🕒 Historique des Rapports Générés")
    for idx, rapport in enumerate(st.session_state.historique, 1):
        st.download_button(
            label=f"📄 Télécharger Rapport {idx}",
            data=rapport["contenu"],
            file_name=rapport["nom"],
            mime="application/pdf",
            use_container_width=True
        )

# --- Sidebar ---
st.sidebar.header("🔍 Détails et Aide")
st.sidebar.markdown("""
1. **Formats acceptés** : PDF, CSV, Excel, Images (PNG, JPG, JPEG).  
2. **Que fait FinAI ?** : Analyse vos fichiers et génère un rapport financier complet.  
3. **Support** : contactez **lydieouattara828@gmail.com**.
""")
