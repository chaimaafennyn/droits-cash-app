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
