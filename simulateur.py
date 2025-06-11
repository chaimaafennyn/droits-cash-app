def calculer_aides(situation, revenu, logement, enfants):
    resultats = {}
    if situation == "Chômage" and revenu < 950:
        resultats["RSA"] = 607
    if logement == "Oui" and revenu < 1200:
        resultats["APL"] = 180
    if situation == "Salarié" and revenu < 1800:
        resultats["Prime d’activité"] = 150
    if situation == "Étudiant" and revenu < 600:
        resultats["Aide spécifique"] = 100
    return resultats
