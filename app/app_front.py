import streamlit as st
import requests
import mimetypes

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