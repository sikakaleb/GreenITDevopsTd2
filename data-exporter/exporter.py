from prometheus_client import start_http_server, Gauge
import json
import time

# Charger les données nettoyées
with open('../data/meteo_nettoyee.json', 'r') as file:
    data = json.load(file)

# Créer des métriques Prometheus
temperature_reelle = Gauge('temperature_reelle', 'Température réelle en °C')
temperature_ressentie = Gauge('temperature_ressentie', 'Température ressentie en °C')
humidite = Gauge('humidite', 'Taux d\'humidité en %')
vent = Gauge('vitesse_du_vent', 'Vitesse du vent en m/s')

# Démarrer le serveur Prometheus sur le port 8000
start_http_server(8000)
print("Exporter Prometheus démarré sur http://localhost:8000")

# Publier les données périodiquement
while True:
    for entry in data:
        temperature_reelle.set(entry['temperature_reelle'])
        temperature_ressentie.set(entry['temperature_ressentie'])
        humidite.set(entry['humidite'])
        vent.set(entry['vent'])
        print(f"Publié : {entry['date']} - Temp: {entry['temperature_reelle']}°C")
        time.sleep(10)  # Attendre 10 secondes avant de publier la prochaine donnée
