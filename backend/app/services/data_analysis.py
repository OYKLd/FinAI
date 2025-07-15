import pandas as pd

def analyze_financial_data(df: pd.DataFrame) -> dict:
    df.columns = [col.strip().lower() for col in df.columns]

    # Conversion des colonnes en float
    df["revenus"] = pd.to_numeric(df["revenus"], errors="coerce").fillna(0)
    df["depenses"] = pd.to_numeric(df["depenses"], errors="coerce").fillna(0)

    revenus = df["revenus"].sum()
    depenses = df["depenses"].sum()
    net = revenus - depenses

    evolution = 0
    if "mois" in df.columns:
        grouped = df.groupby("mois").sum(numeric_only=True)
        if len(grouped) >= 2:
            evolution = round(
                ((grouped["revenus"].iloc[-1] - grouped["revenus"].iloc[0]) / grouped["revenus"].iloc[0]) * 100,
                2
            )

    return {
        "revenus": revenus,
        "depenses": depenses,
        "net": net,
        "evolution": evolution
    }