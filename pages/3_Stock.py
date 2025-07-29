import streamlit as st
import pandas as pd
from utils import charger_json, sauvegarder_json, chemin, get_user_and_role

# 🎨 Couleurs par catégorie
cat_colors = {
    "Fruits": "#FFDDC1",
    "Légumes": "#C1FFD7",
    "Protéines": "#FFD1DC",
    "Produits laitiers": "#D1E0FF",
    "Féculents": "#FFFAC1",
    "Épices": "#FFE0AC",
    "Boissons": "#E0D1FF",
    "Autres": "#F0F0F0"
}


utilisateur, role = get_user_and_role()
chemins = chemin(utilisateur)

stock = charger_json(chemins["stock"], {})
unites = charger_json("unites.json", {})
categories = charger_json("categories.json", {})

st.title("📦 Mon Stock")

unit_choices = ["g", "kg", "ml", "cl", "L", "pcs", "càs", "càc", ""]
cat_choices = ["Fruits", "Légumes", "Protéines", "Produits laitiers", "Féculents", "Épices", "Boissons", "Autres"]

# ➕ Ajouter un ingrédient
st.markdown("### ➕ Ajouter un nouvel ingrédient")
with st.form("ajout_ingredient"):
    new_ingr = st.text_input("Nom de l’ingrédient").strip().lower()
    new_qte = st.number_input("Quantité", min_value=1, step=1)
    new_unit = st.selectbox("Unité", unit_choices, index=0)
    new_cat = st.selectbox("Catégorie", cat_choices, index=0)
    submitted = st.form_submit_button("Ajouter")

    if submitted:
        if not new_ingr:
            st.warning("⛔ Veuillez entrer un nom d’ingrédient.")
        elif new_ingr in stock:
            st.warning("⛔ Cet ingrédient existe déjà dans le stock.")
        else:
            stock[new_ingr] = new_qte
            unites[new_ingr] = new_unit
            categories[new_ingr] = new_cat
            sauvegarder_json(chemins["stock"], stock)
            sauvegarder_json("unites.json", unites)
            sauvegarder_json("categories.json", categories)
            st.success(f"✅ {new_ingr} ajouté avec succès !")
            st.rerun()

# 🎯 Filtrer par catégorie
st.markdown("### 🗂️ Voir stock par catégorie")
cat_selection = st.selectbox("Sélectionner une catégorie", cat_choices)

# 🔍 Filtrer les données
filtered_data = []
for ingr, qte in stock.items():
    cat = categories.get(ingr, "Autres")
    if cat == cat_selection:
        filtered_data.append({
            "Ingrédient": ingr,
            "Quantité": qte,
            "Unité": unites.get(ingr, ""),
            "Catégorie": cat
        })

df = pd.DataFrame(filtered_data)

if df.empty:
    st.info("Aucun ingrédient dans cette catégorie.")
else:
    color = cat_colors.get(cat_selection, "#F0F0F0")
    st.markdown(
        f'<div style="background-color:{color}; padding:15px; border-radius:8px;"><b>{cat_selection}</b> - Ingrédients</div>',
        unsafe_allow_html=True
    )
    st.markdown("### ✏️ Modifier les ingrédients de cette catégorie")

    edited = []
    for i in range(len(df)):
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([4, 2, 2, 1, 1])
            ingr = st.text_input(f"Ingrédient_{i}", df.at[i, "Ingrédient"], key=f"ingr_{i}")
            qte = st.number_input(f"Qté_{i}", 0, 10000, int(df.at[i, "Quantité"]), key=f"qte_{i}")
            unit = st.selectbox(f"Unité_{i}", unit_choices,
                                index=unit_choices.index(df.at[i, "Unité"]) if df.at[i, "Unité"] in unit_choices else 0,
                                key=f"unit_{i}")
            delete = st.checkbox("🗑️", key=f"del_{i}")
            if not delete and ingr.strip():
                edited.append({
                    "Ingrédient": ingr.strip(),
                    "Quantité": qte,
                    "Unité": unit,
                    "Catégorie": cat_selection
                })
            elif delete:
                if ingr in stock:
                    del stock[ingr]
                    unites.pop(ingr, None)
                    categories.pop(ingr, None)

    if st.button("💾 Enregistrer les modifications"):
        new_stock = {row["Ingrédient"]: int(row["Quantité"]) for row in edited}
        new_units = {row["Ingrédient"]: row["Unité"] for row in edited}
        new_cats = {row["Ingrédient"]: row["Catégorie"] for row in edited}

        stock.update(new_stock)
        unites.update(new_units)
        categories.update(new_cats)

        sauvegarder_json(chemins["stock"], stock)
        sauvegarder_json("unites.json", unites)
        sauvegarder_json("categories.json", categories)

        st.success("✅ Données mises à jour avec succès !")
        st.rerun()
