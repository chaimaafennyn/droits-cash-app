import streamlit as st
import pandas as pd
from utils import charger_json, sauvegarder_json

nutrition = charger_json("nutrition.json", {})

st.title("🍎 Valeurs nutritionnelles")

df = pd.DataFrame.from_dict(nutrition, orient='index', columns=["Calories"])
df.index.name = "Aliment"

df_edit = st.data_editor(df, num_rows="dynamic", use_container_width=True)

if st.button("💾 Sauvegarder les valeurs"):
    try:
        df_clean = df_edit.fillna(0).astype(int)
        new_nutri = df_clean["Calories"].to_dict()
        sauvegarder_json("nutrition.json", new_nutri)
        st.success("✅ Données mises à jour")
    except Exception as e:
        st.error(f"❌ Erreur : {e}")
