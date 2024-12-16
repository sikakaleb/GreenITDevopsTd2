import json
import requests
import paho.mqtt.client as mqtt
import time

# Charger les données
with open('./data/donnees_petit.json', 'r') as f:
    data = json.load(f)

# HTTP Configuration
HTTP_URL = "http://http-server:5000/data"

# MQTT Configuration
MQTT_BROKER = "mqtt-broker"
MQTT_PORT = 1883
MQTT_TOPIC = "sensors/data"

mqtt_client = mqtt.Client()

def send_http(data):
    response = requests.post(HTTP_URL, json=data)
    return response.status_code

def send_mqtt(data):
    payload = json.dumps(data)
    mqtt_client.publish(MQTT_TOPIC, payload)
    print(f"MQTT Message Sent: {len(payload)} bytes")

# Envoi des données
print("Sending data via HTTP...")
for item in data:
    send_http(item)
    time.sleep(0.01)  # Simulate a delay

print("Sending data via MQTT...")
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
for item in data:
    send_mqtt(item)
    time.sleep(0.01)  # Simulate a delay
mqtt_client.disconnect()
