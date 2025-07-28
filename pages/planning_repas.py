import streamlit as st
import json
import os
import pandas as pd
import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt

# ---------- CONFIG ----------
FICHIER_JSON = "planning.json"
FICHIER_STOCK = "stock.json"
FICHIER_RECETTES = "recettes.json"
FICHIER_NUTRITION = "nutrition.json"
JOURS_SEMAINE = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# ---------- FONCTIONS ----------

def charger_json(fichier, vide):
    if os.path.exists(fichier):
        with open(fichier, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return vide

def sauvegarder_json(fichier, data):
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generer_pdf(planning_semaine):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Planning de Repas Hebdomadaire", ln=True, align="C")
    pdf.set_font("Arial", '', 12)
    for jour, repas in planning_semaine.items():
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, jour, ln=True)
        pdf.set_font("Arial", '', 12)
        for titre, contenu in repas.items():
            pdf.multi_cell(0, 8, f"- {titre}: {contenu}")
    chemin = "planning_repas.pdf"
    pdf.output(chemin)
    return chemin

def get_week_id(date):
    return date.strftime("%Y-W%U")

# ---------- CHARGEMENT DONNÉES ----------

st.set_page_config(page_title="Planning Repas", layout="wide")
st.title("🍽️ Planificateur de Repas Hebdomadaire (Multi-semaines)")

planning_global = charger_json(FICHIER_JSON, {})
stock = charger_json(FICHIER_STOCK, {})
recettes = charger_json(FICHIER_RECETTES, {})
nutrition = charger_json(FICHIER_NUTRITION, {
    "œufs": 70, "thon": 150, "riz": 200, "pain": 80, "fromage": 90,
    "huile": 120, "banane": 90, "pomme": 80, "lait": 100, "flan": 150
})

# ---------- SÉLECTION DE SEMAINE ----------

date_actuelle = st.date_input("📅 Choisir une date de la semaine")
semaine_id = get_week_id(date_actuelle)
st.markdown(f"### 📆 Semaine sélectionnée : `{semaine_id}`")

if semaine_id not in planning_global:
    planning_global[semaine_id] = {jour: {"Petit-déjeuner": "", "Déjeuner": "", "Dîner": ""} for jour in JOURS_SEMAINE}

planning = planning_global[semaine_id]

# ---------- MODIFICATION PAR JOUR ----------

jours_traduits = {
    "Monday": "Lundi", "Tuesday": "Mardi", "Wednesday": "Mercredi",
    "Thursday": "Jeudi", "Friday": "Vendredi",
    "Saturday": "Samedi", "Sunday": "Dimanche"
}
jour_nom = jours_traduits[date_actuelle.strftime("%A")]

st.subheader(f"🗓️ {jour_nom} : Modifier les repas")
col1, col2, col3 = st.columns(3)
with col1:
    petit_dej = st.text_input("🍞 Petit-déjeuner", value=planning[jour_nom].get("Petit-déjeuner", ""))
with col2:
    dej = st.text_input("🥗 Déjeuner", value=planning[jour_nom].get("Déjeuner", ""))
with col3:
    diner = st.text_input("🍲 Dîner", value=planning[jour_nom].get("Dîner", ""))

if st.button("💾 Enregistrer pour ce jour"):
    planning[jour_nom]["Petit-déjeuner"] = petit_dej
    planning[jour_nom]["Déjeuner"] = dej
    planning[jour_nom]["Dîner"] = diner
    planning_global[semaine_id] = planning
    sauvegarder_json(FICHIER_JSON, planning_global)
    st.success(f"✅ Repas du {jour_nom} enregistré pour {semaine_id}")

# ---------- VUE TABLEAU ----------
st.markdown("---")
st.subheader("📊 Modifier la semaine complète dans un tableau")
df_planning = pd.DataFrame.from_dict(planning, orient='index')
df_edit = st.data_editor(df_planning, num_rows="fixed", use_container_width=True)
if st.button("💾 Enregistrer toute la semaine"):
    planning_modifie = df_edit.to_dict(orient='index')
    planning_global[semaine_id] = planning_modifie
    sauvegarder_json(FICHIER_JSON, planning_global)
    st.success("✅ Planning hebdo enregistré !")

# ---------- SUIVI NUTRITION ----------
st.markdown("---")
st.subheader("🍎 Suivi Nutritionnel (Calories par jour)")
total_calories = {}
for jour, repas in planning.items():
    total = 0
    for texte in repas.values():
        mots = texte.lower().split()
        total += sum(nutrition.get(m.strip(",."), 0) for m in mots)
    total_calories[jour] = total
for jour in JOURS_SEMAINE:
    st.write(f"**{jour}** : {total_calories.get(jour, 0)} kcal")

# ---------- GRAPHIQUE ----------
st.markdown("### 📈 Graphique des calories de la semaine")
fig, ax = plt.subplots()
ax.bar(total_calories.keys(), total_calories.values())
ax.set_ylabel("Calories")
ax.set_title(f"Semaine {semaine_id}")
plt.xticks(rotation=45)
st.pyplot(fig)

# ---------- EXPORT PDF ----------
if st.button("📤 Exporter cette semaine en PDF"):
    chemin = generer_pdf(planning)
    with open(chemin, "rb") as f:
        st.download_button("📄 Télécharger le PDF", f, file_name=f"planning_{semaine_id}.pdf")
