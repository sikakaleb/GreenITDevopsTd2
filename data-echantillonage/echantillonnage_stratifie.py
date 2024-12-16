import json
import numpy as np
import random
from collections import defaultdict


def stratifier_donnees(data, critere):
    """
    Divise les données en strates basées sur un critère donné.

    :param data: Liste de données météo.
    :param critere: Fonction pour catégoriser les données.
    :return: Dictionnaire {strata: liste de données}.
    """
    strates = defaultdict(list)
    for entry in data:
        clé = critere(entry)
        strates[clé].append(entry)
    return strates


def echantillonnage_stratifie(strates, pourcentage):
    """
    Effectue un échantillonnage aléatoire dans chaque strate.

    :param strates: Dictionnaire des strates.
    :param pourcentage: Pourcentage de données à conserver dans chaque strate.
    :return: Liste des données échantillonnées.
    """
    echantillon = []
    for clé, groupe in strates.items():
        taille_echantillon = int(len(groupe) * (pourcentage / 100))
        echantillon.extend(random.sample(groupe, taille_echantillon))
    return echantillon


def calculer_temperature_moyenne(data):
    """
    Calcule la température moyenne réelle et ressentie à partir des données.

    :param data: Liste de données météo.
    :return: Tuple (température réelle moyenne, température ressentie moyenne).
    """
    temperatures_reelles = [entry['temperature_reelle'] for entry in data]
    temperatures_ressenties = [entry['temperature_ressentie'] for entry in data]

    moyenne_reelle = np.mean(temperatures_reelles)
    moyenne_ressentie = np.mean(temperatures_ressenties)

    return moyenne_reelle, moyenne_ressentie


def evaluer_precision(data_originale, data_echantillon):
    """
    Évalue la précision des moyennes calculées sur l'échantillon par rapport aux données originales.

    :param data_originale: Liste complète des données météo.
    :param data_echantillon: Liste échantillonnée des données météo.
    :return: Précision en pourcentage.
    """
    moyenne_reelle_originale, moyenne_ressentie_originale = calculer_temperature_moyenne(data_originale)
    moyenne_reelle_echantillon, moyenne_ressentie_echantillon = calculer_temperature_moyenne(data_echantillon)

    precision_reelle = abs(moyenne_reelle_echantillon - moyenne_reelle_originale) / moyenne_reelle_originale * 100
    precision_ressentie = abs(moyenne_ressentie_echantillon - moyenne_ressentie_originale) / moyenne_ressentie_originale * 100

    moyenne_precision = (precision_reelle + precision_ressentie) / 2

    return moyenne_precision


# Charger les données nettoyées
with open('../data/meteo_nettoyee.json', 'r') as file:
    data_meteo = json.load(file)

# Définir un critère pour les strates (par exemple : intervalles de température)
def critere_temperature(entry):
    temp = entry['temperature_reelle']
    if temp < 0:
        return "T < 0"
    elif 0 <= temp < 10:
        return "0 <= T < 10"
    elif 10 <= temp < 20:
        return "10 <= T < 20"
    else:
        return "T >= 20"

# Stratifier les données
strates = stratifier_donnees(data_meteo, critere_temperature)

# Effectuer un échantillonnage aléatoire dans chaque strate (par exemple, 20%)
pourcentage_echantillon = 20
echantillon_stratifie = echantillonnage_stratifie(strates, pourcentage_echantillon)

# Calculer la précision
precision_stratifie = evaluer_precision(data_meteo, echantillon_stratifie)

# Calcul du ratio quantité de données conservées
quantite_conservee_stratifiee = len(echantillon_stratifie) / len(data_meteo) * 100

print(f"Échantillonnage stratifié:")
print(f"- Données conservées: {len(echantillon_stratifie)} sur {len(data_meteo)} ({quantite_conservee_stratifiee:.2f}%)")
print(f"- Précision moyenne: {precision_stratifie:.2f}%")
