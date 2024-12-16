import json
import datetime
import numpy as np

def echantillonnage_hebdomadaire(data):
    data_par_semaine = {}
    for entry in data:
        date = datetime.datetime.strptime(entry['date'], '%Y-%m-%d')
        semaine = date.isocalendar()[1]
        annee = date.year
        cle = (annee, semaine)
        if cle not in data_par_semaine:
            data_par_semaine[cle] = entry
    return list(data_par_semaine.values())

def echantillonnage_mensuel(data):
    data_par_mois = {}
    for entry in data:
        date = datetime.datetime.strptime(entry['date'], '%Y-%m-%d')
        mois = date.month
        annee = date.year
        cle = (annee, mois)
        if cle not in data_par_mois:
            data_par_mois[cle] = entry
    return list(data_par_mois.values())

def calculer_temperature_moyenne(data):
    temperatures_reelles = [entry['temperature_reelle'] for entry in data]
    temperatures_ressenties = [entry['temperature_ressentie'] for entry in data]

    moyenne_reelle = np.mean(temperatures_reelles)
    moyenne_ressentie = np.mean(temperatures_ressenties)

    return moyenne_reelle, moyenne_ressentie

def evaluer_precision(data_originale, data_echantillon):
    moyenne_reelle_originale, moyenne_ressentie_originale = calculer_temperature_moyenne(data_originale)
    moyenne_reelle_echantillon, moyenne_ressentie_echantillon = calculer_temperature_moyenne(data_echantillon)

    precision_reelle = abs(moyenne_reelle_echantillon - moyenne_reelle_originale) / moyenne_reelle_originale * 100
    precision_ressentie = abs(moyenne_ressentie_echantillon - moyenne_ressentie_originale) / moyenne_ressentie_originale * 100

    moyenne_precision = (precision_reelle + precision_ressentie) / 2

    return moyenne_precision

# Charger les données nettoyées
with open('../data/meteo_nettoyee.json', 'r') as file:
    data_meteo = json.load(file)

# Trier les données par date
data_meteo.sort(key=lambda x: x['date'])

# Échantillonnage hebdomadaire
echantillon_hebdo = echantillonnage_hebdomadaire(data_meteo)
precision_hebdo = evaluer_precision(data_meteo, echantillon_hebdo)
quantite_conservee_hebdo = len(echantillon_hebdo) / len(data_meteo) * 100

print(f"Échantillonnage hebdomadaire:")
print(f"- Données conservées: {len(echantillon_hebdo)} sur {len(data_meteo)} ({quantite_conservee_hebdo:.2f}%)")
print(f"- Précision moyenne: {precision_hebdo:.2f}%")

# Échantillonnage mensuel
echantillon_mensuel = echantillonnage_mensuel(data_meteo)
precision_mensuelle = evaluer_precision(data_meteo, echantillon_mensuel)
quantite_conservee_mensuelle = len(echantillon_mensuel) / len(data_meteo) * 100

print(f"\nÉchantillonnage mensuel:")
print(f"- Données conservées: {len(echantillon_mensuel)} sur {len(data_meteo)} ({quantite_conservee_mensuelle:.2f}%)")
print(f"- Précision moyenne: {precision_mensuelle:.2f}%")
