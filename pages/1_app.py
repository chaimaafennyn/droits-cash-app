import streamlit as st
import json
import os

# ---------- FONCTIONS UTILITAIRES ----------

FICHIER_JSON = "planning.json"

# Charger ou créer planning
def charger_planning():
    if os.path.exists(FICHIER_JSON):
        with open(FICHIER_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
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

# Sauvegarder dans le fichier
def sauvegarder_planning(data):
    with open(FICHIER_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ---------- INTERFACE STREAMLIT ----------

st.title("🍽️ Planificateur de Repas Hebdomadaire")

# Charger données
planning = charger_planning()

# Sélection du jour
jour = st.selectbox("Choisis un jour :", list(planning.keys()))
est_travail = st.checkbox("Est-ce un jour de travail ?", value=(jour in ["Mardi", "Mercredi"]))

st.subheader(f"Modifier les repas du {jour} :")

# Champs de modification
petit_dej = st.text_input("🍞 Petit-déjeuner", value=planning[jour].get("Petit-déjeuner", ""))
dej = st.text_input("🥗 Déjeuner", value=planning[jour].get("Déjeuner (à emporter)", "") if est_travail else planning[jour].get("Déjeuner", ""))
diner = st.text_input("🍲 Dîner", value=planning[jour].get("Dîner", ""))

# Sauvegarde
if st.button("💾 Enregistrer les modifications"):
    if est_travail:
        planning[jour]["Déjeuner (à emporter)"] = dej
        if "Déjeuner" in planning[jour]:
            planning[jour].pop("Déjeuner")
    else:
        planning[jour]["Déjeuner"] = dej
        if "Déjeuner (à emporter)" in planning[jour]:
            planning[jour].pop("Déjeuner (à emporter)")

    planning[jour]["Petit-déjeuner"] = petit_dej
    planning[jour]["Dîner"] = diner
    sauvegarder_planning(planning)
    st.success(f"✅ Repas du {jour} mis à jour avec succès !")

# ---------- Affichage recettes (bonus) ----------
recettes = {
    "Soupe tomate": "Faire revenir un oignon, ajouter 1 càs concentré tomate, eau, sel, cumin, un peu de kheli3, cuire 10 min.",
    "Quiche sans pâte": "Mélanger 2 œufs, 1 verre de lait, 1 càs maïzena, oignon, fromage. Cuire au four 20 min à 180°C.",
    "Nouilles sautées": "Faire revenir oignon + tomate concentrée, ajouter nouilles cuites, œuf battu, sauter 5 min."
}

st.markdown("---")
recette_du_jour = st.selectbox("📖 Voir une recette :", list(recettes.keys()))
st.markdown(f"**Recette :** {recettes[recette_du_jour]}")
