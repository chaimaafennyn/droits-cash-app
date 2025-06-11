# simulateur.py
from data import aides_data

def calculer_aides(situation, revenu, logement, enfants):
    resultats = {}
    for aide in aides_data:
        if aide["conditions"](situation, revenu, logement, enfants):
            resultats[aide["nom"]] = aide["montant"]
    return resultats
