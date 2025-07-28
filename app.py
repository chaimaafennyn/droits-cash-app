import streamlit as st

# Jours de la semaine
jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# Repas pré-remplis (extrait simplifié)
planning = {
    "Mardi": {
        "Petit-déjeuner": "Pain + Vache qui rit + thé + dattes",
        "Déjeuner (à emporter)": "Salade PDT + thon + concombre + olives",
        "Dîner": "Nouilles sautées + œuf + tomate concentrée"
    },
    # tu complètes avec les autres jours...
}

# Interface
st.title("Mon Plan de Repas de la Semaine")

jour = st.selectbox("Choisis un jour", jours)

if jour in planning:
    st.subheader(f"Repas du {jour}")
    for repas, contenu in planning[jour].items():
        st.write(f"**{repas}** : {contenu}")
else:
    st.write("Aucun repas défini pour ce jour.")

if st.checkbox("Afficher recette du dîner"):
    st.markdown("**Recette Nouilles sautées** :\n- Nouilles + oignons + concentré tomate + œuf\n- Sauter à la poêle 5-7 min.")

