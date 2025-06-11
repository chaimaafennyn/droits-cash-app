# data.py
aides_data = [
    {
        "nom": "RSA",
        "conditions": lambda s, r, l, e: s == "Chômage" and r < 950,
        "montant": 607
    },
    {
        "nom": "APL",
        "conditions": lambda s, r, l, e: l == "Oui" and r < 1200,
        "montant": 180
    },
    {
        "nom": "Prime d’activité",
        "conditions": lambda s, r, l, e: s == "Salarié" and r < 1800,
        "montant": 150
    },
    {
        "nom": "Aide étudiante spécifique",
        "conditions": lambda s, r, l, e: s == "Étudiant" and r < 600,
        "montant": 100
    },
]

