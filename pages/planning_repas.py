import streamlit as st
import json
import os
import pandas as pd
import datetime
from fpdf import FPDF

# ---------- CONFIG ----------
FICHIER_JSON = "planning.json"
JOURS_SEMAINE = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# ---------- FONCTIONS ----------

def charger_planning():
    if os.path.exists(FICHIER_JSON):
        with open(FICHIER_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {jour: {"Petit-déjeuner": "", "Déjeuner": "", "Dîner": ""} for jour in JOURS_SEMAINE}

def sauvegarder_planning(data):
    with open(FICHIER_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generer_pdf(planning):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Planning de Repas Hebdomadaire", ln=True, align="C")
    pdf.set_font("Arial", '', 12)
    for jour, repas in planning.items():
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, jour, ln=True)
        pdf.set_font("Arial", '', 12)
        for titre, contenu in repas.items():
            pdf.multi_cell(0, 8, f"- {titre}: {contenu}")
    chemin = "planning_repas.pdf"
    pdf.output(chemin)
    return chemin

# ---------- INTERFACE STREAMLIT ----------

st.set_page_config(page_title="Planning Repas", layout="wide")
st.title("🍽️ Planificateur de Repas Hebdomadaire avec Calendrier")

# Chargement et date
planning = charger_planning()
semaine_actuelle = st.date_input("📅 Choisir un jour de la semaine", datetime.date.today())
# Traduction des jours en français
jours_traduits = {
    "Monday": "Lundi",
    "Tuesday": "Mardi",
    "Wednesday": "Mercredi",
    "Thursday": "Jeudi",
    "Friday": "Vendredi",
    "Saturday": "Samedi",
    "Sunday": "Dimanche"
}

jour_en = semaine_actuelle.strftime("%A")
jour_nom = jours_traduits.get(jour_en, "Lundi")


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
    sauvegarder_planning(planning)
    st.success(f"✅ Repas du {jour_nom} mis à jour")

st.markdown("---")
st.subheader("📋 Vue complète de la semaine")

# Tableau interactif semaine
edited = False
for jour in JOURS_SEMAINE:
    with st.expander(f"📅 {jour}"):
        col1, col2, col3 = st.columns(3)
        with col1:
            pdj = st.text_input(f"Petit-déj - {jour}", value=planning[jour]["Petit-déjeuner"], key=f"pdj_{jour}")
        with col2:
            dj = st.text_input(f"Déjeuner - {jour}", value=planning[jour]["Déjeuner"], key=f"dej_{jour}")
        with col3:
            dn = st.text_input(f"Dîner - {jour}", value=planning[jour]["Dîner"], key=f"diner_{jour}")
        planning[jour]["Petit-déjeuner"] = pdj
        planning[jour]["Déjeuner"] = dj
        planning[jour]["Dîner"] = dn
        edited = True

if st.button("💾 Enregistrer toute la semaine"):
    sauvegarder_planning(planning)
    st.success("✅ Semaine mise à jour avec succès")

# Liste de courses
if st.button("🛒 Générer une liste de courses"):
    ingredients = []
    for repas in planning.values():
        for desc in repas.values():
            mots = desc.lower().replace(",", "").split()
            ingredients.extend(mots)
    stopwords = {"+", "de", "du", "la", "et", "le", "un", "avec", "ou", "des"}
    courses = sorted(set([m for m in ingredients if len(m) > 3 and m not in stopwords]))
    st.markdown("### Liste de courses :")
    for item in courses:
        st.write(f"- {item}")

# Export PDF
if st.button("📤 Exporter le planning en PDF"):
    chemin = generer_pdf(planning)
    with open(chemin, "rb") as f:
        st.download_button("📄 Télécharger le PDF", f, file_name="planning_repas.pdf")
