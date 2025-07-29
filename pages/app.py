import streamlit as st
import json
import os
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from fpdf import FPDF

# ---------- UTILISATEUR CONNECTÉ ----------
if "utilisateur" not in st.session_state:
    st.error("⚠️ Veuillez vous connecter via main.py")
    st.stop()
utilisateur = st.session_state["utilisateur"]
role = st.session_state["role"]

if "confirm_logout" not in st.session_state:
    st.session_state["confirm_logout"] = False


# ---------- CHEMINS PAR UTILISATEUR ----------
def chemin(nom):
    return {
        "planning": f"planning_{nom}.json",
        "stock": f"stock_{nom}.json",
    }

# ---------- GESTION JSON ----------
def charger_json(fichier, vide):
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            contenu = f.read().strip()
            return json.loads(contenu) if contenu else vide
    except (json.JSONDecodeError, FileNotFoundError):
        return vide

def sauvegarder_json(fichier, data):
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ---------- INTERFACE ----------
st.set_page_config(page_title="App Repas", layout="centered")
st.title(f"👋 Bienvenue {utilisateur} ({role})")

# ---------- ADMIN : Liste des utilisateurs ----------
if role == "admin":
    st.sidebar.subheader("👥 Comptes utilisateurs")
    fichiers = [f for f in os.listdir() if f.startswith("planning_") and f.endswith(".json")]
    noms = [f.replace("planning_", "").replace(".json", "") for f in fichiers]
    cible = st.sidebar.selectbox("📂 Voir le planning de :", noms)
else:
    cible = utilisateur

# ---------- CHARGEMENT DONNÉES ----------
chemins = chemin(cible)
planning = charger_json(chemins["planning"], {})
stock = charger_json(chemins["stock"], {})
recettes = charger_json("recettes.json", {})
nutrition = charger_json("nutrition.json", {
    "œufs": 70, "thon": 150, "riz": 200, "pain": 80, "fromage": 90,
    "huile": 120, "banane": 90, "pomme": 80, "lait": 100, "flan": 150
})

JOURS_SEMAINE = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

def get_week_id(date):
    return date.strftime("%Y-W%U")

date_actuelle = st.date_input("📅 Choisir une date")
semaine_id = get_week_id(date_actuelle)
st.markdown(f"### 📆 Semaine sélectionnée : `{semaine_id}`")

if semaine_id not in planning:
    planning[semaine_id] = {jour: {"Petit-déjeuner": "", "Déjeuner": "", "Dîner": ""} for jour in JOURS_SEMAINE}

planning_semaine = planning[semaine_id]

# ---------- MODIFICATION PAR JOUR ----------
jour_nom = date_actuelle.strftime("%A")
fr_jour = {
    "Monday": "Lundi", "Tuesday": "Mardi", "Wednesday": "Mercredi",
    "Thursday": "Jeudi", "Friday": "Vendredi", "Saturday": "Samedi", "Sunday": "Dimanche"
}[jour_nom]

st.subheader(f"🗓️ Modifier les repas du {fr_jour}")
petit = st.text_area("🍞 Petit-déjeuner", planning_semaine[fr_jour].get("Petit-déjeuner", ""))
dej = st.text_area("🥗 Déjeuner", planning_semaine[fr_jour].get("Déjeuner", ""))
diner = st.text_area("🍲 Dîner", planning_semaine[fr_jour].get("Dîner", ""))

if st.button("💾 Enregistrer ce jour"):
    planning_semaine[fr_jour] = {
        "Petit-déjeuner": petit,
        "Déjeuner": dej,
        "Dîner": diner
    }
    planning[semaine_id] = planning_semaine
    sauvegarder_json(chemins["planning"], planning)
    st.success(f"✅ {fr_jour} enregistré pour {cible}")

# ---------- SUIVI CALORIQUE ----------
st.markdown("---")
st.subheader("🍎 Suivi Nutritionnel")
objectif = st.number_input("Objectif kcal/jour", 0, 10000, 2000, 50)
calories = {}
for jour, repas in planning_semaine.items():
    total = 0
    for texte in repas.values():
        mots = texte.lower().split()
        total += sum(nutrition.get(m.strip(",."), 0) for m in mots)
    calories[jour] = total

for jour in JOURS_SEMAINE:
    kcal = calories.get(jour, 0)
    if kcal > objectif:
        st.error(f"❌ {jour} : {kcal} kcal")
    else:
        st.success(f"✅ {jour} : {kcal} kcal")

fig, ax = plt.subplots()
ax.bar(calories.keys(), calories.values(), color=["red" if v > objectif else "green" for v in calories.values()])
ax.axhline(y=objectif, color='blue', linestyle='--')
ax.set_ylabel("Calories")
ax.set_title("Calories par jour")
st.pyplot(fig)

# ---------- STOCK ----------
st.markdown("---")
st.subheader("📦 Mon Stock")
if not stock:
    df_stock = pd.DataFrame(columns=["Ingrédient", "Quantité"])
else:
    df_stock = pd.DataFrame([{"Ingrédient": k, "Quantité": v} for k, v in stock.items()])

df_stock_edit = st.data_editor(df_stock, num_rows="dynamic", use_container_width=True)

if st.button("💾 Enregistrer le stock"):
    try:
        stock_mod = df_stock_edit.dropna()
        stock_simple = {
            str(row["Ingrédient"]).strip(): int(row["Quantité"])
            for _, row in stock_mod.iterrows()
            if str(row["Ingrédient"]).strip() != "" and int(row["Quantité"]) > 0
        }
        sauvegarder_json(chemins["stock"], stock_simple)
        st.success("✅ Stock mis à jour")
    except Exception as e:
        st.error(f"❌ Erreur dans les données : {e}")



# ---------- RECETTES ----------
st.markdown("---")
st.subheader("📘 Mes Recettes")
if recettes:
    for nom, ingr in recettes.items():
        st.markdown(f"**{nom}** : {', '.join(ingr)}")
else:
    st.info("Aucune recette enregistrée.")

# ---------- AJOUT DE RECETTES ----------
st.markdown("---")
st.subheader("➕ Ajouter une recette")
nom_recette = st.text_input("Nom de la recette")
ingr_recette = st.text_input("Ingrédients (séparés par des virgules)")
if st.button("Ajouter la recette"):
    if nom_recette and ingr_recette:
        liste = [i.strip().lower() for i in ingr_recette.split(",") if i.strip()]
        recettes[nom_recette] = liste
        sauvegarder_json("recettes.json", recettes)
        st.success("✅ Recette ajoutée !")
    else:
        st.error("Remplis les champs.")

# ---------- SUGGESTIONS ----------
st.markdown("---")
st.subheader("🤖 Recettes possibles avec mon stock")
recettes_possibles = []
for nom, ingredients in recettes.items():
    if all(ing in stock for ing in ingredients):
        kcal = sum(nutrition.get(ing, 0) for ing in ingredients)
        if kcal <= objectif:
            recettes_possibles.append((nom, kcal))

if recettes_possibles:
    for nom, kcal in recettes_possibles:
        st.markdown(f"**{nom}** ({kcal} kcal)")
        jour = st.selectbox("Jour", JOURS_SEMAINE, key=f"jour_{nom}")
        moment = st.selectbox("Moment", ["Petit-déjeuner", "Déjeuner", "Dîner"], key=f"moment_{nom}")
        if st.button(f"📥 Ajouter {nom}", key=f"btn_{nom}"):
            planning_semaine[jour][moment] = nom
            planning[semaine_id] = planning_semaine
            sauvegarder_json(chemins["planning"], planning)
            st.success(f"✅ Ajouté à {moment} du {jour}")
else:
    st.info("Aucune recette réalisable avec ton stock.")

# ---------- MODIFIER NUTRITION ----------
st.markdown("---")
st.subheader("⚙️ Modifier valeurs nutritionnelles")
df_nutri = pd.DataFrame.from_dict(nutrition, orient='index', columns=['Calories'])
df_nutri.index.name = 'Aliment'
df_nutri_edit = st.data_editor(df_nutri, num_rows="dynamic", use_container_width=True)
if st.button("💾 Sauvegarder les valeurs"):
    nutri_mod = df_nutri_edit.fillna(0).to_dict(orient='index')
    nutri_simple = {k: int(v['Calories']) for k, v in nutri_mod.items() if v['Calories'] > 0}
    sauvegarder_json("nutrition.json", nutri_simple)
    st.success("✅ Nutrition mise à jour")

# ---------- EXPORT ----------
def generer_pdf(planning):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Planning de Repas", ln=True, align="C")
    pdf.set_font("Arial", '', 12)
    for jour, repas in planning.items():
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, jour, ln=True)
        pdf.set_font("Arial", '', 12)
        for titre, contenu in repas.items():
            pdf.multi_cell(0, 8, f"- {titre}: {contenu}")
    chemin = f"planning_{cible}_{semaine_id}.pdf"
    pdf.output(chemin)
    return chemin

if st.button("📤 Exporter PDF"):
    pdf_file = generer_pdf(planning_semaine)
    with open(pdf_file, "rb") as f:
        st.download_button("📄 Télécharger", f, file_name=pdf_file)

# ---------- DÉCONNEXION ----------
if st.sidebar.button("🚪 Se déconnecter"):
    st.session_state["confirm_logout"] = True

if st.session_state["confirm_logout"]:
    with st.sidebar.expander("❓ Confirmer la déconnexion", expanded=True):
        st.write("Voulez-vous vraiment vous déconnecter ?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Oui, déconnecter"):
                st.session_state.clear()
                st.success("✅ Déconnexion réussie ! Redirection...")
                st.switch_page("main.py")  # Redirige vers la page de login
        with col2:
            if st.button("❌ Annuler"):
                st.session_state["confirm_logout"] = False

