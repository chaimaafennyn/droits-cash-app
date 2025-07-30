import json
import os

import streamlit as st

def verifier_connexion():
    if "utilisateur" not in st.session_state:
        st.error("⚠️ Vous devez vous connecter depuis la page principale.")
        st.stop()
    return st.session_state["utilisateur"], st.session_state["role"]


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
    except (json.JSONDecodeError, FileNotFoundError):
        return vide

def sauvegarder_json(fichier, data):
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user_and_role():
    import streamlit as st
    if "utilisateur" not in st.session_state:
        st.error("⚠️ Veuillez vous connecter via main.py")
        st.stop()
    return st.session_state["utilisateur"], st.session_state["role"]
