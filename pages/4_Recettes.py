import streamlit as st
from utils import charger_json, sauvegarder_json, chemin, get_user_and_role

utilisateur, role = get_user_and_role()
chemins = chemin(utilisateur)

recettes = charger_json("recettes.json", {})
stock = charger_json(chemins["stock"], {})
courses = charger_json(chemins["courses"], [])
planning = charger_json(chemins["planning"], {})
nutrition = charger_json("nutrition.json", {})

JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
objectif = st.number_input("🎯 Objectif kcal/jour", 0, 10000, 2000, 50)

st.title("📘 Mes Recettes")

# Affichage des recettes existantes
if recettes:
    for nom, ingr in recettes.items():
        st.markdown(f"**{nom}** : {', '.join(ingr)}")
else:
    st.info("Aucune recette enregistrée.")

# Ajout de recette
st.markdown("---")
st.subheader("➕ Ajouter une recette")
nom = st.text_input("Nom de la recette")
ingrs = st.text_input("Ingrédients (séparés par des virgules)")
if st.button("Ajouter la recette"):
    if nom and ingrs:
        recettes[nom] = [i.strip().lower() for i in ingrs.split(",") if i.strip()]
        sauvegarder_json("recettes.json", recettes)
        st.success("✅ Recette ajoutée")
        st.rerun()
    else:
        st.error("❗ Remplis tous les champs.")

# Suggestions
st.markdown("---")
st.subheader("🤖 Recettes possibles avec mon stock")
possibles = []
for nom, ing_list in recettes.items():
    if all(ing in stock for ing in ing_list):
        kcal = sum(nutrition.get(ing, 0) for ing in ing_list)
        if kcal <= objectif:
            possibles.append((nom, kcal))

if possibles:
    for nom, kcal in possibles:
        st.markdown(f"**{nom}** – {kcal} kcal")
        jour = st.selectbox("Jour", JOURS, key=f"jour_{nom}")
        moment = st.selectbox("Moment", ["Petit-déjeuner", "Déjeuner", "Dîner"], key=f"moment_{nom}")
        if st.button(f"📥 Ajouter {nom}", key=f"add_{nom}"):
            semaine_id = st.date_input("Date de la semaine").strftime("%Y-W%U")
            if semaine_id not in planning:
                planning[semaine_id] = {j: {"Petit-déjeuner": "", "Déjeuner": "", "Dîner": ""} for j in JOURS}
            planning[semaine_id][jour][moment] = nom
            sauvegarder_json(chemins["planning"], planning)

            # Déduire les ingrédients
            for ing in recettes[nom]:
                if ing in stock:
                    stock[ing] -= 1
                    if stock[ing] == 0:
                        del stock[ing]
                        if ing not in courses:
                            courses.append(ing)
            sauvegarder_json(chemins["stock"], stock)
            sauvegarder_json(chemins["courses"], courses)

            st.success(f"✅ {nom} ajouté à {moment} du {jour}")
            st.rerun()
else:
    st.info("Aucune recette réalisable actuellement.")
