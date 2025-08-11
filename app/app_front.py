import streamlit as st
import requests
import mimetypes
import pandas as pd
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="FinAI - Analyse Financière", layout="centered", initial_sidebar_state="collapsed")
st.title("🌟 **FinAI - Générateur de Rapport Financier** 🌟")

# Description de l'application avec un style plus dynamique
st.markdown("""
Bienvenue sur **FinAI**, l'outil qui vous permet de générer rapidement des rapports financiers à partir de vos fichiers. Téléchargez votre fichier et laissez FinAI faire le reste !
""", unsafe_allow_html=True)

# Initialiser l'historique en mémoire
if "historique" not in st.session_state:
    st.session_state.historique = []

# Choix du fichier
st.write("### 📂 **Téléchargez votre fichier**")
allowed_extensions = ["pdf", "csv", "xls", "xlsx", "png", "jpg", "jpeg"]

uploaded_files = st.file_uploader(
    "Choisissez un fichier (PDF, Excel, CSV, ou Image)",
    type=allowed_extensions,
    label_visibility="collapsed",
    accept_multiple_files=False
)

# --- Nouvelle section : Données utilisateur et graphiques ---
st.write("\n---\n")
st.write("### 📊 **Entrez ou importez vos propres données pour générer des graphiques**")

data_file = st.file_uploader(
    "Importer un fichier de données (CSV ou Excel)",
    type=["csv", "xlsx"],
    key="data_uploader"
)

df = None
if data_file:
    try:
        if data_file.name.endswith('.csv'):
            df = pd.read_csv(data_file)
        else:
            df = pd.read_excel(data_file)
        # Conversion des colonnes numériques
        for col in df.columns[1:]:  # On suppose que la première colonne est 'Mois'
            df[col] = df[col].astype(str).str.replace(" ", "").str.replace("\u00A0", "").str.replace(",", ".")
            df[col] = pd.to_numeric(df[col], errors='coerce')
        st.success("✅ Données chargées avec succès !")
        st.write("Aperçu des données :")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")

if df is not None:
    st.write("#### 📈 Visualisation de vos données :")
    chart_type = st.selectbox(
        "Choisissez le type de graphique",
        ("Lignes (toutes les colonnes numériques)", "Camembert (pie chart)")
    )

    if chart_type == "Lignes (toutes les colonnes numériques)":
        try:
            numeric_cols = df.select_dtypes(include='number').columns
            if len(numeric_cols) == 0:
                st.warning("Aucune colonne numérique trouvée dans vos données. Impossible de générer un graphique automatique.")
            else:
                fig, ax = plt.subplots()
                df[numeric_cols].plot(ax=ax)
                st.pyplot(fig)
                fig.savefig("app/graphique_utilisateur.png")
                st.info("Le graphique a été généré et peut être inclus dans le rapport.")
        except Exception as e:
            st.error(f"Erreur lors de la génération du graphique : {e}")
    else:
        # Camembert : l'utilisateur choisit la colonne à représenter
        col = st.selectbox(
            "Choisissez la colonne à représenter en camembert",
            options=[c for c in df.columns if c != df.columns[0]]
        )
        try:
            fig, ax = plt.subplots()
            ax.pie(df[col], labels=df[df.columns[0]], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)
            fig.savefig("app/graphique_utilisateur.png")
            st.info("Le graphique a été généré et peut être inclus dans le rapport.")
        except Exception as e:
            st.error(f"Erreur lors de la génération du camembert : {e}")

# Si un fichier est téléchargé
if uploaded_files:
    with st.spinner("🌀 **Analyse en cours...**"):
        mime_type, _ = mimetypes.guess_type(uploaded_files.name)
        if mime_type is None:
            mime_type = "application/octet-stream"
        
        files = [("files", (uploaded_files.name, uploaded_files, mime_type))]

        try:
            response = requests.post("http://localhost:8000/analyze/", files=files)
            if response.status_code == 200:
                st.success("✅ **Rapport généré avec succès !**")

                # Sauvegarder l'historique
                st.session_state.historique.append({
                    "nom": "rapport_financier.pdf",
                    "contenu": response.content
                })

                st.download_button(
                    label="📥 **Télécharger le rapport PDF**",
                    data=response.content,
                    file_name="rapport_financier.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                st.error(f"⚠️ **Erreur lors de la génération du rapport :** {response.text}")
        except Exception as e:
            st.error(f"❌ **Erreur de connexion à l'API :** {e}")

# Affichage de l'historique
if st.session_state.historique:
    st.subheader("🕒 **Historique des Rapports Générés**")
    for idx, rapport in enumerate(st.session_state.historique, 1):
        st.download_button(
            label=f"📄 **Télécharger Rapport {idx}**",
            data=rapport["contenu"],
            file_name=rapport["nom"],
            mime="application/pdf",
            use_container_width=True
        )

# Sidebar pour informations complémentaires
st.sidebar.header("🔍 **Détails et Aide**")
st.sidebar.markdown("""
1. **Formats acceptés** : PDF, CSV, Excel, Images (PNG, JPG, JPEG).
2. **Que fait FinAI ?** : FinAI analyse vos fichiers et génère un rapport financier complet.
3. **Aide en cas de problème** : Si vous rencontrez un problème, contactez notre support à **lydieouattara828@gmail.com**.
""")