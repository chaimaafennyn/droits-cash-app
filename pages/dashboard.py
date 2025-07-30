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
st.markdown("- 📅 [Planning des repas](./planning.py)")
st.markdown("- 📦 [Mon stock](./stock)")
st.markdown("- 🛒 [Ma liste de courses](./courses)")
st.markdown("- 📘 [Mes recettes](./recettes)")
st.markdown("- 🍎 [Suivi nutritionnel](./nutrition)")
st.markdown("- 🧾 [Exporter PDF](./export)")

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
