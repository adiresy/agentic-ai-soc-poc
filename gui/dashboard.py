import streamlit as st
import pandas as pd
from datetime import datetime

# Imports depuis le package src
from src.collector import collect_logs
from src.siem import index_events
from src.ueba import detect_anomalies
from src.agent import soc_agent

# --------------------------------------------------
# Configuration générale de la page
# --------------------------------------------------
st.set_page_config(
    page_title="Agent IA Assistant SOC – POC",
    layout="wide"
)

st.title("🛡️ Agent IA Assistant SOC – Proof of Concept")

st.markdown("""
### Principe fondamental  
👉 **L’IA recommande, l’humain décide**
""")

st.markdown("""
Ce tableau de bord illustre une **chaîne SOC simplifiée**, depuis des données
de démonstration interopérables jusqu’aux recommandations IA,
avec **validation humaine obligatoire**.
""")

# --------------------------------------------------
# Bouton de lancement de l'analyse
# --------------------------------------------------
if st.button("▶ Lancer l’analyse SOC"):

    # -------------------------------
    # INPUT – Données de démonstration
    # -------------------------------
    st.subheader("📥 Données d’entrée (INPUT)")
    events = collect_logs()
    st.write(f"{len(events)} événement(s) chargé(s)")

    # -------------------------------
    # TRAITEMENTS
    # -------------------------------
    st.subheader("⚙️ Traitements (PROCESSING)")

    indexed_events = index_events(events)
    alerts = detect_anomalies(indexed_events)
    recommendations = soc_agent(alerts)

    if not recommendations:
        st.success("✅ Aucune anomalie détectée.")
    else:
        st.warning(f"⚠️ {len(recommendations)} alerte(s) détectée(s)")

    # -------------------------------
    # OUTPUT – Recommandations & décisions
    # -------------------------------
    st.subheader("📤 Recommandations IA & décisions humaines (OUTPUT)")

    table_rows = []

    for i, rec in enumerate(recommendations):
        st.markdown(f"#### Alerte {i+1}")

        st.write("**Type d’alerte :**", rec["summary"])
        st.write("**Recommandation IA :**", rec["recommendation"])
        st.write("**Niveau de confiance IA :**", rec["confidence"])

        decision = st.selectbox(
            "Décision de l’analyste",
            ["Non traitée", "Validée", "Rejetée"],
            key=f"decision_{i}"
        )

        table_rows.append({
            "Horodatage décision": datetime.utcnow().isoformat(),
            "Timestamp événement": rec["event"]["timestamp"],
            "Actif": rec["event"]["asset"],
            "Type d’alerte": rec["summary"],
            "Recommandation IA": rec["recommendation"],
            "Confiance IA": rec["confidence"],
            "Décision analyste": decision
        })

    # --------------------------------------------------
    # Tableau de synthèse
    # --------------------------------------------------
    if table_rows:
        df_decisions = pd.DataFrame(table_rows)

        st.subheader("📊 Tableau de synthèse SOC")
        st.dataframe(df_decisions, use_container_width=True)

        # --------------------------------------------------
        # Export CSV
        # --------------------------------------------------
        csv = df_decisions.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Télécharger les décisions (CSV)",
            data=csv,
            file_name="decisions_soc_poc.csv",
            mime="text/csv"
        )

# ----------------------------------------

