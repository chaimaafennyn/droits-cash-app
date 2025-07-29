import streamlit as st
import pandas as pd
from utils import charger_json, sauvegarder_json, chemin, get_user_and_role

utilisateur, role = get_user_and_role()
chemins = chemin(utilisateur)

stock = charger_json(chemins["stock"], {})
unites = charger_json("unites.json", {})
categories = charger_json("categories.json", {})

st.title("📦 Mon Stock")

unit_choices = ["g", "kg", "ml", "cl", "L", "pcs", "càs", "càc", ""]
cat_choices = ["Fruits", "Légumes", "Protéines", "Produits laitiers", "Féculents", "Épices", "Boissons", "Autres"]

stock_data = []
for ingr, qte in stock.items():
    stock_data.append({
        "Ingrédient": ingr,
        "Quantité": qte,
        "Unité": unites.get(ingr, ""),
        "Catégorie": categories.get(ingr, "")
    })

df = pd.DataFrame(stock_data)

edited = []
st.markdown("### ✏️ Modifier stock, unité et catégorie")
for i in range(len(df)):
    col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
    ingr = st.text_input(f"Ingrédient_{i}", df.at[i, "Ingrédient"], key=f"ingr_{i}")
    qte = st.number_input(f"Quantité_{i}", 0, 10000, int(df.at[i, "Quantité"]), key=f"qte_{i}")
    unit = st.selectbox(f"Unité_{i}", unit_choices, index=unit_choices.index(df.at[i, "Unité"]) if df.at[i, "Unité"] in unit_choices else 0, key=f"unit_{i}")
    cat = st.selectbox(f"Catégorie_{i}", cat_choices, index=cat_choices.index(df.at[i, "Catégorie"]) if df.at[i, "Catégorie"] in cat_choices else 0, key=f"cat_{i}")
    if ingr.strip():
        edited.append({"Ingrédient": ingr.strip(), "Quantité": qte, "Unité": unit, "Catégorie": cat})

if st.button("💾 Enregistrer le stock"):
    new_stock = {row["Ingrédient"]: int(row["Quantité"]) for row in edited if row["Quantité"] > 0}
    new_units = {row["Ingrédient"]: row["Unité"] for row in edited}
    new_cats = {row["Ingrédient"]: row["Catégorie"] for row in edited}

    sauvegarder_json(chemins["stock"], new_stock)
    sauvegarder_json("unites.json", new_units)
    sauvegarder_json("categories.json", new_cats)

    st.success("✅ Données enregistrées !")
    st.rerun()


# ---------- COURSES ----------
st.markdown("---")
st.subheader("🛍️ Mes Courses")

st.markdown("### Ingrédients à acheter")
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
    st.info("Aucune course enregistrée")

nouvel_ing = st.text_input("Ajouter un ingrédient à acheter")
if st.button("➕ Ajouter à mes courses"):
    if nouvel_ing and nouvel_ing not in courses and nouvel_ing not in stock:
        courses.append(nouvel_ing.strip())
        sauvegarder_json(chemins["courses"], courses)
        st.success("✅ Ingrédient ajouté aux courses")
    else:
        st.warning("⛔ Déjà dans les stocks ou les courses")


