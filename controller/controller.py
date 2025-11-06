import time
import json
import random
import csv
from paho.mqtt import client as mqtt_client

MQTT_BROKER = "mosquitto-service"
MQTT_PORT = 1883
SENSOR_TOPIC = "irrigation/sensordata"
ACT_TOPIC = "irrigation/actions"

MOISTURE_THRESHOLD = 30
HUMIDITY_THRESHOLD = 40

client = mqtt_client.Client()

# Retry connecting to broker
while True:
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        break
    except Exception:
        print("Waiting for MQTT broker, retrying in 5 seconds...")
        time.sleep(5)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(SENSOR_TOPIC)

fieldnames = ['sensor_id', 'irrigate', 'energy_used', 'data_processed', 'timestamp']

with open('controller_action_log.csv', 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if csvfile.tell() == 0:
        writer.writeheader()

    def on_message(client, userdata, msg):
        data = json.loads(msg.payload.decode())
        print("Received:", data)
        action_needed = (data['soil_moisture'] < MOISTURE_THRESHOLD) or (data['humidity'] < HUMIDITY_THRESHOLD)
        # Simulate random energy and data for the irrigation decision
        energy_used = round(random.uniform(0.05, 0.2), 3)    # Joules, change as needed
        data_processed = round(random.uniform(0.1, 0.7), 2)  # MB, change as needed
        action = {
            "sensor_id": data["sensor_id"],
            "irrigate": action_needed,
            "energy_used": energy_used,
            "data_processed": data_processed,
            "timestamp": data["timestamp"]
        }
        client.publish(ACT_TOPIC, json.dumps(action))
        print("Action published:", action)
        writer.writerow(action)

    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_forever()

