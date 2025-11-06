import time
import random
import json
import csv
from paho.mqtt import client as mqtt_client

MQTT_BROKER = "mosquitto-service"
MQTT_PORT = 1883

client = mqtt_client.Client()

while True:
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        break
    except Exception as e:
        print("Waiting for MQTT broker, retrying in 5 seconds...")
        time.sleep(5)

TOPIC = "irrigation/sensordata"

with open('sensor_data_log.csv', 'a', newline='') as csvfile:
    fieldnames = ['sensor_id', 'temperature', 'humidity', 'soil_moisture', 'energy_used', 'data_processed', 'timestamp']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if csvfile.tell() == 0:
        writer.writeheader()

    while True:
        # Simulate random values for energy used and data processed (Mb)
        energy_used = round(random.uniform(0.01, 0.05), 3)    # Joules, change as appropriate
        data_processed = round(random.uniform(0.1, 0.5), 2)   # MB, change as appropriate
        data = {
            "sensor_id": f"sensor_{random.randint(1, 10)}",
            "temperature": round(random.uniform(22, 36), 2),
            "humidity": round(random.uniform(30, 80), 2),
            "soil_moisture": round(random.uniform(10, 60), 2),
            "energy_used": energy_used,
            "data_processed": data_processed,
            "timestamp": time.time()
        }
        client.publish(TOPIC, json.dumps(data))
        print(f"Published: {data}")
        writer.writerow(data)
        time.sleep(2)

