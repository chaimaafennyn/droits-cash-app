import streamlit as st
import json
import os
import pandas as pd
import datetime
from fpdf import FPDF

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

planning = charger_json(FICHIER_JSON, {jour: {"Petit-déjeuner": "", "Déjeuner": "", "Dîner": ""} for jour in JOURS_SEMAINE})
stock = charger_json(FICHIER_STOCK, {})
recettes = charger_json(FICHIER_RECETTES, {})
nutrition = charger_json(FICHIER_NUTRITION, {
    "œufs": 70, "thon": 150, "riz": 200, "pain": 80, "fromage": 90,
    "huile": 120, "banane": 90, "pomme": 80, "lait": 100, "flan": 150
})

jours_traduits = {
    "Monday": "Lundi",
    "Tuesday": "Mardi",
    "Wednesday": "Mercredi",
    "Thursday": "Jeudi",
    "Friday": "Vendredi",
    "Saturday": "Samedi",
    "Sunday": "Dimanche"
}

semaine_actuelle = st.date_input("📅 Choisir un jour de la semaine", datetime.date.today())
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
    sauvegarder_json(FICHIER_JSON, planning)
    st.success(f"✅ Repas du {jour_nom} mis à jour")

# ---------- Vue tableau interactive ----------
st.markdown("---")
st.subheader("📊 Modifier toute la semaine dans un tableau")
df_planning = pd.DataFrame.from_dict(planning, orient='index')
df_edit = st.data_editor(df_planning, num_rows="fixed", use_container_width=True)
if st.button("💾 Enregistrer les modifications du tableau"):
    planning_modifie = df_edit.to_dict(orient='index')
    sauvegarder_json(FICHIER_JSON, planning_modifie)
    st.success("✅ Planning modifié via le tableau !")

# ---------- Liste de courses ----------
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

# ---------- Stock des ingrédients ----------
st.markdown("---")
st.subheader("📦 Mon Stock d'ingrédients")
df_stock = pd.DataFrame.from_dict(stock, orient='index', columns=['Quantité'])
df_stock.index.name = 'Ingrédient'
df_stock_edit = st.data_editor(df_stock, num_rows="dynamic", use_container_width=True)
if st.button("💾 Enregistrer mon stock"):
    stock_modifie = df_stock_edit.fillna(0).to_dict(orient='index')
    stock_simplifie = {k: int(v['Quantité']) for k, v in stock_modifie.items() if v['Quantité'] > 0}
    sauvegarder_json(FICHIER_STOCK, stock_simplifie)
    st.success("✅ Stock mis à jour avec succès")

# ---------- Suggestions de repas ----------
st.markdown("---")
st.subheader("🤖 Suggestions de repas selon mon stock")
recettes_utiles = recettes.copy()

recettes_possibles = []
for nom, ingredients in recettes_utiles.items():
    if all(ing in stock for ing in ingredients):
        recettes_possibles.append(nom)

if recettes_possibles:
    st.success("🍽️ Tu peux préparer :")
    for r in recettes_possibles:
        with st.expander(r):
            st.write(", ".join(recettes[r]))
            jour_choix = st.selectbox(f"📆 Choisir un jour pour ajouter '{r}'", JOURS_SEMAINE, key=f"sel_{r}")
            moment = st.selectbox("🕒 Choisir un moment", ["Petit-déjeuner", "Déjeuner", "Dîner"], key=f"moment_{r}")
            if st.button(f"📥 Ajouter '{r}' au planning", key=f"add_{r}"):
                planning[jour_choix][moment] = r
                sauvegarder_json(FICHIER_JSON, planning)
                st.success(f"✅ '{r}' ajouté à {moment} de {jour_choix}")
else:
    st.info("Aucune recette trouvée avec ton stock actuel. Ajoute d'autres ingrédients !")

# ---------- Ajout de recettes personnalisées ----------
st.markdown("---")
st.subheader("📘 Ajouter une nouvelle recette")
nom_recette = st.text_input("Nom de la recette")
ingredients_recette = st.text_input("Ingrédients (séparés par des virgules)")

if st.button("➕ Ajouter la recette"):
    if nom_recette and ingredients_recette:
        ingredients_liste = [ing.strip().lower() for ing in ingredients_recette.split(",") if ing.strip()]
        recettes[nom_recette] = ingredients_liste
        sauvegarder_json(FICHIER_RECETTES, recettes)
        st.success(f"✅ Recette '{nom_recette}' ajoutée avec succès !")
    else:
        st.error("Merci de remplir le nom et les ingrédients.")

# ---------- Visualisation des recettes ----------
st.markdown("---")
st.subheader("📚 Toutes mes recettes enregistrées")
if recettes:
    for nom, ingr in recettes.items():
        st.markdown(f"**{nom}** : {', '.join(ingr)}")
else:
    st.info("Aucune recette enregistrée pour l'instant.")

# ---------- Suivi nutritionnel ----------
st.markdown("---")
st.subheader("🍎 Suivi Nutritionnel (calories approximatives)")

valeurs_par_aliment = nutrition

total_calories = {}
for jour, repas in planning.items():
    total = 0
    for texte in repas.values():
        mots = texte.lower().split()
        total += sum(valeurs_par_aliment.get(m.strip(",."), 0) for m in mots)
    total_calories[jour] = total

st.markdown("### Calories estimées par jour :")
for jour in JOURS_SEMAINE:
    st.write(f"**{jour}** : {total_calories.get(jour, 0)} kcal")

# ---------- Édition des valeurs nutritionnelles ----------
st.markdown("---")
st.subheader("⚙️ Modifier les valeurs nutritionnelles par aliment")
df_nutrition = pd.DataFrame.from_dict(valeurs_par_aliment, orient='index', columns=['Calories'])
df_nutrition.index.name = 'Aliment'
df_nutrition_edit = st.data_editor(df_nutrition, num_rows="dynamic", use_container_width=True)
if st.button("💾 Enregistrer les calories"):
    nutri_modifie = df_nutrition_edit.fillna(0).to_dict(orient='index')
    nutrition_simplifie = {k: int(v['Calories']) for k, v in nutri_modifie.items() if v['Calories'] > 0}
    sauvegarder_json(FICHIER_NUTRITION, nutrition_simplifie)
    st.success("✅ Valeurs nutritionnelles mises à jour")

# ---------- Export PDF ----------
if st.button("📤 Exporter le planning en PDF"):
    chemin = generer_pdf(planning)
    with open(chemin, "rb") as f:
        st.download_button("📄 Télécharger le PDF", f, file_name="planning_repas.pdf")
