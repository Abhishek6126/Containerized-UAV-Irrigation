from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import random
import time
import math

ENDPOINT = "a1z1sc7i-ats.iot.eu-north-1.amazonaws.com"  # e.g., "a3k7odshaiipe8-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "SimulatedSensorClient"
TOPIC = "sensor_data"

CA_PATH = "./AmazonRootCA1.pem"
CERT_PATH = "./492db43f54e8ef9898a12341c24b53a31ef49e0ffb7f4f99c0ca0-certificate.pem.crt"
KEY_PATH = "./492d64c2c5f15a2bf4f99c0ca0-private.pem.key"

mqtt_client = AWSIoTMQTTClient(CLIENT_ID)
mqtt_client.configureEndpoint(ENDPOINT, 8883)
mqtt_client.configureCredentials(CA_PATH, KEY_PATH, CERT_PATH)

mqtt_client.configureOfflinePublishQueueing(-1)
mqtt_client.configureDrainingFrequency(2)
mqtt_client.configureConnectDisconnectTimeout(10)
mqtt_client.configureMQTTOperationTimeout(5)

mqtt_client.connect()

base_soil = 0.25
base_humidity = 60
samples = 100
interval = 2

for t in range(samples):
    soil_moisture = base_soil + 0.05 * math.sin(2 * math.pi * t / 24) + random.uniform(-0.01, 0.01)
    soil_moisture = max(0.10, min(0.40, soil_moisture))

    air_humidity = base_humidity + 10 * math.cos(2 * math.pi * t / 24) + random.uniform(-2, 2)
    air_humidity = max(30, min(90, air_humidity))

    payload = json.dumps({
        "timestamp": t,
        "soil_moisture": round(soil_moisture, 3),
        "air_humidity": round(air_humidity, 1)
    })

    mqtt_client.publish(TOPIC, payload, 1)
    print(f"Published: {payload}")
    time.sleep(interval)

mqtt_client.disconnect()

