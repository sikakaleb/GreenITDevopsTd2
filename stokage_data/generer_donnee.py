import json
import random
from datetime import datetime, timedelta

def generer_donnee(date):
    """
    Génère une donnée météo aléatoire pour une date donnée.
    """
    return {
        "date": date.strftime('%Y-%m-%d %H:%M:%S'),
        "temperature_reelle": round(random.uniform(-10, 35), 1),  # Température réelle entre -10 et 35 °C
        "temperature_ressentie": round(random.uniform(-15, 40), 1),  # Température ressentie entre -15 et 40 °C
        "humidite": random.randint(10, 100),  # Humidité en %
        "vent": round(random.uniform(0, 20), 1)  # Vitesse du vent en m/s
    }

def generer_jeu_donnees(n_points, fichier_sortie):
    """
    Génère un jeu de données JSON avec n_points et l'écrit dans un fichier.
    """
    date_debut = datetime(2024, 1, 1, 0, 0, 0)
    donnees = []

    for i in range(n_points):
        # Incrémenter les dates de manière aléatoire
        date_actuelle = date_debut + timedelta(minutes=i * random.randint(1, 10))
        donnees.append(generer_donnee(date_actuelle))

    # Écriture dans un fichier
    with open(fichier_sortie, 'w') as fichier:
        json.dump(donnees, fichier, indent=4)
    print(f"Jeu de données de {n_points} points écrit dans {fichier_sortie}")

# Génération des jeux de données
generer_jeu_donnees(10_000, "../data/donnees_petit.json")  # Petit volume
generer_jeu_donnees(1_000_000, "../data/donnees_moyen.json")  # Volume moyen
generer_jeu_donnees(50_000_000, "../data/donnees_gros.json")  # Gros volume
