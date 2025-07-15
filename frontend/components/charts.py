import streamlit as st
import pandas as pd
import plotly.express as px

def show_charts(df: pd.DataFrame):
    st.subheader("📈 Visualisation des données")

    if "mois" in df.columns:
        try:
            df["mois"] = pd.to_datetime(df["mois"])
        except Exception:
            pass

        fig = px.line(df, x="mois", y=["revenus", "depenses"], title="Évolution des revenus et dépenses")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Colonne 'mois' manquante pour afficher le graphique.")