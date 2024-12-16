import json
import random
import numpy as np


def echantillonner_donnees(data, pourcentage):
    """
    Sélectionne aléatoirement un pourcentage de données.

    :param data: Liste de données météo.
    :param pourcentage: Pourcentage de données à conserver (entre 0 et 100).
    :return: Liste de données échantillonnées.
    """
    taille_echantillon = int(len(data) * (pourcentage / 100))
    return random.sample(data, taille_echantillon)


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


def evaluer_precision(data_originale, pourcentage, iterations=5):
    """
    Évalue la précision moyenne sur plusieurs itérations d'échantillonnage.

    :param data_originale: Liste complète des données météo.
    :param pourcentage: Pourcentage de données à conserver.
    :param iterations: Nombre d'itérations pour la moyenne.
    :return: Précision moyenne entre les moyennes calculées sur l'échantillon et l'ensemble des données.
    """
    moyenne_reelle_originale, moyenne_ressentie_originale = calculer_temperature_moyenne(data_originale)

    precisions = []
    for _ in range(iterations):
        echantillon = echantillonner_donnees(data_originale, pourcentage)
        moyenne_reelle_echantillon, moyenne_ressentie_echantillon = calculer_temperature_moyenne(echantillon)

        precision_reelle = abs(moyenne_reelle_echantillon - moyenne_reelle_originale) / moyenne_reelle_originale * 100
        precision_ressentie = abs(moyenne_ressentie_echantillon - moyenne_ressentie_originale) / moyenne_ressentie_originale * 100

        moyenne_precision = (precision_reelle + precision_ressentie) / 2
        precisions.append(moyenne_precision)

    return np.mean(precisions)


def tester_pourcentages(data, pourcentages):
    """
    Teste plusieurs pourcentages pour trouver le meilleur ratio précision/quantité.

    :param data: Liste de données météo.
    :param pourcentages: Liste de pourcentages à tester.
    :return: Dictionnaire {pourcentage: précision moyenne}.
    """
    resultats = {}
    for pourcentage in pourcentages:
        precision_moyenne = evaluer_precision(data, pourcentage)
        resultats[pourcentage] = precision_moyenne
        print(f"Pourcentage: {pourcentage}% -> Précision moyenne: {precision_moyenne:.2f}%")
    return resultats


# Charger les données nettoyées
with open('../data/meteo_nettoyee.json', 'r') as file:
    data_meteo = json.load(file)

# Tester avec différents pourcentages
pourcentages_testes = [1, 2, 5, 10, 20, 50, 80, 100]
resultats_finales = tester_pourcentages(data_meteo, pourcentages_testes)

# Trouver le meilleur pourcentage
meilleur_pourcentage = min(resultats_finales, key=lambda x: resultats_finales[x])
print(f"\nLe meilleur ratio précision/quantité est obtenu avec {meilleur_pourcentage}% des données.")
