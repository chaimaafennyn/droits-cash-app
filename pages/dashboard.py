import streamlit as st
from utils import get_user_and_role

# Récupérer l'utilisateur et son rôle
utilisateur, role = get_user_and_role()

# Page de bienvenue
st.set_page_config(page_title="Accueil", layout="centered")
st.title("🏠 Tableau de bord")
st.markdown(f"👋 Bonjour **{utilisateur}** ({role}) !")

st.markdown("---")

# Sections accessibles
st.subheader("📌 Navigation rapide")
st.markdown("- 📅 [Planning des repas](./Planning.py)")
st.markdown("- 📦 [Mon stock](./Stock)")
st.markdown("- 🛒 [Ma liste de courses](./Courses)")
st.markdown("- 📘 [Mes recettes](./Recettes)")
st.markdown("- 🍎 [Suivi nutritionnel](./Nutrition)")
st.markdown("- 🧾 [Exporter PDF](./Export)")

# Admin uniquement
if role == "admin":
    st.markdown("---")
    st.subheader("🔐 Zone admin")
    st.markdown("- 👥 [Gestion utilisateurs](./utilisateurs)")

# Déconnexion rapide
if st.button("🚪 Se déconnecter"):
    st.session_state.clear()
    st.success("Déconnexion réussie.")
    st.switch_page("main.py")
