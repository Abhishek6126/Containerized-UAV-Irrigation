import random
import time
import math

# Parameters
base_soil = 0.25     # base/starting soil moisture (fraction, e.g. 0.25 = 25%)
base_humidity = 60   # base/starting air humidity (%)
samples = 100        # number of readings/time steps
interval = 2         # seconds between readings

for t in range(samples):
    # Simulate soil moisture as random walk + sine/cosine
    soil_moisture = base_soil + 0.05 * math.sin(2 * math.pi * t / 24) + random.uniform(-0.01, 0.01)
    soil_moisture = max(0.10, min(0.40, soil_moisture))  # clamp to 10-40%

    # Simulate air humidity as cyclic (day/night) + small noise
    air_humidity = base_humidity + 10 * math.cos(2 * math.pi * t / 24) + random.uniform(-2, 2)
    air_humidity = max(30, min(90, air_humidity))        # clamp to 30-90%

    print(f"Sample {t}: Soil Moisture={soil_moisture:.3f}  Air Humidity={air_humidity:.1f}")
    time.sleep(interval)  # Wait before next reading
