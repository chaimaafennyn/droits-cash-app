import streamlit as st
import json
import os
import datetime

from utils import verifier_connexion
utilisateur, role = verifier_connexion()


def chemin(nom):
    return {
        "planning": f"planning_{nom}.json",
        "stock": f"stock_{nom}.json",
        "courses": f"courses_{nom}.json"
    }

def charger_json(fichier, vide):
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            contenu = f.read().strip()
            return json.loads(contenu) if contenu else vide
    except:
        return vide

def sauvegarder_json(fichier, data):
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)




if role == "admin":
    st.sidebar.subheader("👥 Comptes utilisateurs")
    fichiers = [f for f in os.listdir() if f.startswith("planning_") and f.endswith(".json")]
    noms = [f.replace("planning_", "").replace(".json", "") for f in fichiers]
    cible = st.sidebar.selectbox("📂 Voir le planning de :", noms)
else:
    cible = utilisateur

chemins = chemin(cible)
planning = charger_json(chemins["planning"], {})
stock = charger_json(chemins["stock"], {})
courses = charger_json(chemins["courses"], [])

JOURS_SEMAINE = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

def get_week_id(date):
    return date.strftime("%Y-W%U")

date_actuelle = st.date_input("📅 Choisir une date")
semaine_id = get_week_id(date_actuelle)
st.markdown(f"### 📆 Semaine sélectionnée : `{semaine_id}`")

if semaine_id not in planning:
    planning[semaine_id] = {jour: {"Petit-déjeuner": "", "Déjeuner": "", "Dîner": ""} for jour in JOURS_SEMAINE}
planning_semaine = planning[semaine_id]

jour_nom = date_actuelle.strftime("%A")
fr_jour = {
    "Monday": "Lundi", "Tuesday": "Mardi", "Wednesday": "Mercredi",
    "Thursday": "Jeudi", "Friday": "Vendredi", "Saturday": "Samedi", "Sunday": "Dimanche"
}[jour_nom]

st.subheader(f"🗓️ Modifier les repas du {fr_jour}")
all_ingredients = list(stock.keys()) + courses

def nettoyer_default(valeur, options):
    if isinstance(valeur, list):
        cleaned = valeur
    elif isinstance(valeur, str):
        cleaned = [i.strip() for i in valeur.split(",") if i.strip()]
    else:
        cleaned = []
    return [v for v in cleaned if v in options]

petit = st.multiselect("🍞 Petit-déjeuner", options=all_ingredients,
                       default=nettoyer_default(planning_semaine[fr_jour].get("Petit-déjeuner", ""), all_ingredients),
                       format_func=lambda x: f"✅ {x}" if x in stock else (f"❌ {x}" if x in courses else x))

dej = st.multiselect("🥗 Déjeuner", options=all_ingredients,
                     default=nettoyer_default(planning_semaine[fr_jour].get("Déjeuner", ""), all_ingredients),
                     format_func=lambda x: f"✅ {x}" if x in stock else (f"❌ {x}" if x in courses else x))

diner = st.multiselect("🍲 Dîner", options=all_ingredients,
                       default=nettoyer_default(planning_semaine[fr_jour].get("Dîner", ""), all_ingredients),
                       format_func=lambda x: f"✅ {x}" if x in stock else (f"❌ {x}" if x in courses else x))

if st.button("📏 Enregistrer ce jour"):
    repas_du_jour = {
        "Petit-déjeuner": petit,
        "Déjeuner": dej,
        "Dîner": diner
    }

    planning_semaine[fr_jour] = {k: ", ".join(v) for k, v in repas_du_jour.items()}
    planning[semaine_id] = planning_semaine
    sauvegarder_json(chemins["planning"], planning)

    for liste_ingredients in repas_du_jour.values():
        for ingr in liste_ingredients:
            if ingr in stock and stock[ingr] > 0:
                stock[ingr] -= 1
                if stock[ingr] == 0:
                    del stock[ingr]
                    if ingr not in courses:
                        courses.append(ingr)

    sauvegarder_json(chemins["stock"], stock)
    sauvegarder_json(chemins["courses"], courses)

    st.success(f"✅ {fr_jour} enregistré pour {cible} et stock mis à jour.")
    st.rerun()
