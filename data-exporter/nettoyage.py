import json

# Charger le fichier JSON brut
with open('../data/meteo.json', 'r') as file:
    data = json.load(file)

# Extraire les informations pertinentes à partir de la clé "days"
donnees_nettoyees = []
for entry in data['days']:  # Parcourir la liste des jours
    donnees_nettoyees.append({
        'date': entry['datetime'],  # Date
        'temperature_reelle': entry['temp'],  # Température réelle moyenne
        'temperature_ressentie': entry['feelslike'],  # Température ressentie moyenne
        'humidite': entry['humidity'],  # Humidité
        'vent': entry['windspeed']  # Vitesse du vent
    })

# Sauvegarder les données nettoyées dans un nouveau fichier JSON
with open('meteo_nettoyee.json', 'w') as file:
    json.dump(donnees_nettoyees, file, indent=4)

print("Fichier nettoyé sauvegardé : 'meteo_nettoyee.json'.")
