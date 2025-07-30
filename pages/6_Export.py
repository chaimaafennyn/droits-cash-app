
import streamlit as st
from fpdf import FPDF
import datetime
from utils import chemin, charger_json, get_user_and_role

# --- Authentification
utilisateur, role = get_user_and_role()
chemins = chemin(utilisateur)

# --- Chargement du planning
planning = charger_json(chemins["planning"], {})

# --- Sélection de la semaine
def get_week_id(date):
    return date.strftime("%Y-W%U")

date_actuelle = st.date_input("📅 Choisir une date", datetime.date.today())
semaine_id = get_week_id(date_actuelle)
st.markdown(f"### 🗓️ Semaine sélectionnée : `{semaine_id}`")

if semaine_id not in planning:
    st.warning("⚠️ Aucun planning enregistré pour cette semaine.")
    st.stop()

planning_semaine = planning[semaine_id]

# --- Génération du PDF
def generer_pdf(planning_semaine, semaine_id):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"Planning de repas – Semaine {semaine_id}", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", '', 12)
    for jour, repas in planning_semaine.items():
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"{jour}", ln=True)
        pdf.set_font("Arial", '', 12)
        for moment, contenu in repas.items():
            pdf.multi_cell(0, 8, f"• {moment} : {contenu}")
        pdf.ln(5)

    nom_fichier = f"planning_{utilisateur}_{semaine_id}.pdf"
    pdf.output(nom_fichier)
    return nom_fichier

# --- Bouton de téléchargement
if st.button("📤 Générer le PDF du planning"):
    fichier = generer_pdf(planning_semaine, semaine_id)
    with open(fichier, "rb") as f:
        st.download_button("📄 Télécharger le planning", f, file_name=fichier)
