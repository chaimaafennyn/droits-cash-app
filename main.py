import streamlit as st
import json
import os
import hashlib

# ---------- CONFIG ----------
USERS_FILE = "users.json"

# ---------- UTILS ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def charger_utilisateurs():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def sauvegarder_utilisateurs(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def authentifier(login, mot_de_passe):
    utilisateurs = charger_utilisateurs()
    if login in utilisateurs and utilisateurs[login]["mdp"] == hash_password(mot_de_passe):
        return utilisateurs[login]["role"]
    return None

def charger_json(fichier, vide):
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            contenu = f.read().strip()
            return json.loads(contenu) if contenu else vide
    except (json.JSONDecodeError, FileNotFoundError):
        return vide


# ---------- INITIALISATION ----------
utilisateurs = charger_utilisateurs()
if "chaimaa" not in utilisateurs:
    utilisateurs["chaimaa"] = {"mdp": hash_password("admin"), "role": "admin"}
    sauvegarder_utilisateurs(utilisateurs)

# ---------- INTERFACE CONNEXION ----------
st.set_page_config(page_title="Connexion")
st.title("🔐 Connexion à l'application de repas")

onglet = st.sidebar.radio("Navigation", ["Connexion", "Inscription"])

if onglet == "Connexion":
    st.subheader("👤 Connexion")
    login = st.text_input("Nom d'utilisateur")
    mot_de_passe = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        role = authentifier(login, mot_de_passe)
        if role:
            st.session_state["utilisateur"] = login
            st.session_state["role"] = role
            st.success(f"Bienvenue {login} !")
            st.switch_page("pages/app.py")  # Redirection vers l'app principale
        else:
            st.error("Identifiants incorrects")

elif onglet == "Inscription":
    st.subheader("📝 Inscription")
    new_login = st.text_input("Choisir un nom d'utilisateur")
    new_password = st.text_input("Choisir un mot de passe", type="password")
    if st.button("Créer le compte"):
        if new_login in utilisateurs:
            st.warning("Ce nom d'utilisateur existe déjà.")
        else:
            utilisateurs[new_login] = {"mdp": hash_password(new_password), "role": "utilisateur"}
            sauvegarder_utilisateurs(utilisateurs)
            st.success("Compte créé avec succès. Vous pouvez vous connecter.")
