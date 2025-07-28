import streamlit as st
import json

# -----------------------------
# Donnees : Planning complet
# -----------------------------
planning = {
    "Mardi": {
        "Petit-déjeuner": "Pain + Vache qui rit + thé + dattes",
        "Déjeuner (à emporter)": "Salade pommes de terre + thon + concombre + olives",
        "Dîner": "Nouilles sautées + œuf + tomate concentrée"
    },
    "Mercredi": {
        "Petit-déjeuner": "Corn flakes + lait + 1 banane",
        "Déjeuner (à emporter)": "Sandwich omelette + kheli3 + pain",
        "Dîner": "Velouté tomate + tartine fromage + yaourt"
    },
    "Jeudi": {
        "Petit-déjeuner": "Pain + miel + thé à la menthe + dattes",
        "Déjeuner": "Quiche sans pâte + salade tomate/concombre",
        "Dîner": "Soupe tomate + pain + œuf dur + flan"
    },
    "Vendredi": {
        "Petit-déjeuner": "Corn flakes + lait + amandes",
        "Déjeuner": "Nouilles sautées + kheli3 + oignons",
        "Dîner": "Salade pommes de terre + olives + yaourt"
    },
    "Samedi": {
        "Petit-déjeuner": "Pain + Vache qui rit + café + dattes",
        "Déjeuner": "Omelette + pommes de terre sautées + salade",
        "Dîner": "Soupe tomate + pain + kheli3 + flan"
    },
    "Dimanche": {
        "Petit-déjeuner": "Corn flakes + lait + 1 banane",
        "Déjeuner": "Salade thon + œuf dur + tomates + olives + pain",
        "Dîner": "Soupe légère + tartine fromage + glace"
    }
}

# -----------------------------
# Interface utilisateur
# -----------------------------
st.title("🍽️ Planificateur de Repas Hebdomadaire")

jour = st.selectbox("Choisis un jour :", list(planning.keys()))
est_travail = st.checkbox("Est-ce un jour de travail ?", value=(jour in ["Mardi", "Mercredi"]))

st.subheader(f"Repas du {jour}")
for repas, contenu in planning[jour].items():
    st.write(f"**{repas}** : {contenu}")

# -----------------------------
# Recettes simples (extrait)
# -----------------------------
recettes = {
    "Soupe tomate": "Faire revenir un oignon, ajouter 1 càs de concentré de tomate, eau, sel, cumin, un peu de kheli3 (optionnel), cuire 10 min.",
    "Quiche sans pâte": "Mélanger 2 œufs, 1 verre de lait, 1 càs maïzena, oignon, fromage. Cuire au four 20 min à 180°C.",
    "Nouilles sautées": "Faire revenir oignon + tomate concentrée, ajouter les nouilles cuites, 1 œuf battu, sauter 5 min."
}

recette_du_jour = st.selectbox("Voir la recette de :", list(recettes.keys()))
st.markdown(f"**Recette :** {recettes[recette_du_jour]}")

# -----------------------------
# Liste de courses auto (option simple)
# -----------------------------
if st.button("📋 Générer liste de courses basique"):
    courses = [
        "Pommes de terre", "Tomates", "Concombres", "Oignons", "Œufs", "Lait",
        "Pain", "Thon", "Fromage Vache qui rit", "Dattes", "Flan", "Corn flakes",
        "Yaourts", "Nouilles chinoises", "Maïzena", "Glace", "Amandes", "Banane"
    ]
    st.markdown("### Liste de courses :")
    for item in courses:
        st.write(f"- {item}")
