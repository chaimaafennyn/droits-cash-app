import streamlit as st
from simulateur import calculer_aides
from pdf_generator import generer_pdf

st.set_page_config(page_title="Droits+Cash", layout="centered")
st.title("💶 Droits+Cash – Simulation d’aides sociales")

with st.form("formulaire_aides"):
    situation = st.selectbox("Ta situation :", ["Étudiant", "Salarié", "Chômage", "RSA", "Sans emploi"])
    revenu = st.number_input("Tes revenus mensuels (€)", min_value=0)
    logement = st.radio("Es-tu locataire ?", ["Oui", "Non"])
    enfants = st.number_input("Nombre d'enfants", min_value=0)
    envoyer = st.form_submit_button("🔎 Voir mes droits")

if envoyer:
    st.subheader("📊 Résultat de la simulation")
    aides = calculer_aides(situation, revenu, logement, enfants)
    if not aides:
        st.warning("Aucune aide estimée dans ta situation actuelle.")
    else:
        for aide, montant in aides.items():
            st.success(f"✅ {aide} : environ {montant} €/mois")

        if st.button("📄 Générer mon dossier PDF"):
            pdf_bytes = generer_pdf(situation, revenu, logement, enfants, aides)
            st.download_button("📥 Télécharger le dossier PDF", data=pdf_bytes, file_name="droits_cash.pdf")
