import paho.mqtt.client as paho
import json
import time
import random
import sys
from datetime import datetime

broker = "localhost"
port = 1883

# Interval in seconds between each data publication
publish_interval = 5

# Function called when data is published
def on_publish(client, userdata, result):
    print(f"Data published to {userdata['topic']}: {userdata['message']}")
    pass

# Create MQTT client
client = paho.Client()
client.on_publish = on_publish

# Connect to MQTT broker
client.connect(broker, port)

# Continuous data simulation
try:
    while True:
        # Get the current time
        current_time = datetime.now().time()

        # Generate random values for temperature and humidity
        # Temperature between 15 and 30 degrees Celsius
        temperature = random.uniform(15, 30)
        # Humidity between 30% and 70%
        humidity = random.uniform(30, 70)
        
        # Determine the light status based on the current time
        light = 1 if 10 <= current_time.hour < 18 else 0
        
        # Generate a random value for the presence of people
        # Presence of people (1) or none (0)
        presence = random.choice([0, 1])

        # Structure of the message to be sent
        data = {
            "id": sys.argv[1],
            "temperature": temperature,
            "humidity": humidity,
            "light": light,
            "presence": presence
        }

        # Publish data to the MQTT topic (such as 'office/lobby')
        topic = f"office/{sys.argv[1]}"
        message = json.dumps(data)
        # Store message and topic in userdata before publishing
        client.user_data_set({"topic": topic, "message": message})
        result = client.publish(topic, message)
        
        # Wait for the established interval before the next publication
        time.sleep(publish_interval)
except KeyboardInterrupt:
    print("Simulation terminated")
    client.disconnect()