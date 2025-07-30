
import streamlit as st
from utils import charger_json, sauvegarder_json, chemin

from utils import verifier_connexion

utilisateur, role = verifier_connexion()


utilisateur, role = get_user_and_role()
chemins = chemin(utilisateur)
stock = charger_json(chemins["stock"], {})
courses = charger_json(chemins["courses"], [])

st.title("🛒 Mes Courses")

st.markdown("### 📋 Liste des ingrédients à acheter")
if courses:
    for ingr in courses:
        col1, col2, col3 = st.columns([5, 2, 2])
        with col1:
            st.write(ingr)
        with col2:
            if st.button("✅ Acheté", key=f"achete_{ingr}"):
                stock[ingr] = stock.get(ingr, 0)
                courses.remove(ingr)
                sauvegarder_json(chemins["stock"], stock)
                sauvegarder_json(chemins["courses"], courses)
                st.rerun()
        with col3:
            if st.button("🗑️ Supprimer", key=f"suppr_{ingr}"):
                courses.remove(ingr)
                sauvegarder_json(chemins["courses"], courses)
                st.rerun()
else:
    st.info("✅ Aucun ingrédient à acheter.")

nouvel_ing = st.text_input("Ajouter un ingrédient à acheter")
if st.button("➕ Ajouter à mes courses"):
    if nouvel_ing and nouvel_ing not in courses and nouvel_ing not in stock:
        courses.append(nouvel_ing.strip())
        sauvegarder_json(chemins["courses"], courses)
        st.success("✅ Ingrédient ajouté")
    else:
        st.warning("⛔ Déjà présent dans le stock ou les courses.")


