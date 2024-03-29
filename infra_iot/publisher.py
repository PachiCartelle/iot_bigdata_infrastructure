import paho.mqtt.client as paho
import json
import time
import random
import sys
from datetime import datetime

broker = "localhost"
port = 1883

# Interval in seconds between each data publication
publish_interval = 15

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

        # Generate values for lighting
        # Determine the light status based on the current time
        light = 1 if 10 <= current_time.hour < 18 else 0
        
        # Generate a random value for the presence of people
        # Presence of people (1) or none (0)
        presence = random.choice([0, 1])

        # obtain room value from the argument
        room = sys.argv[1]

        # Specific configurations of temperature and humidity
        # for each room, using random values in a given range
        if room == 'outside':
            # in case of outside, temperature depends on current time
            if 10 <= current_time.hour < 19:
                temperature = random.uniform(10, 15)
            elif 19 <= current_time.hour < 24:
                temperature = random.uniform(7, 10)
            else:
                temperature = random.uniform(5, 8)
            humidity = random.uniform(60, 80)
        elif room == 'lobby':
            temperature = random.uniform(18, 21)
            humidity = random.uniform(55, 70)
        elif room in ['office1', 'office2']:
            temperature = random.uniform(19, 22)
            humidity = random.uniform(45, 60)
        elif room == 'conference_room':
            # in case of conference room, temperature  and humidity
            # depends on presence of people on the room
            if presence == 1:
                temperature = random.uniform(22, 25)
                humidity = random.uniform(55, 75)
            else:
                temperature = random.uniform(18, 20)
                humidity = random.uniform(45, 60)

        # Structure of the message to be sent
        data = {
            "id": room,
            "temperature": temperature,
            "humidity": humidity,
            "light": light,
            "presence": presence
        }

        # Publish data to the MQTT topic (such as 'office/lobby')
        topic = f"office/{room}"
        message = json.dumps(data)
        # Store message and topic in userdata before publishing
        client.user_data_set({"topic": topic, "message": message})
        result = client.publish(topic, message)
        
        # Wait for the established interval before the next publication
        time.sleep(publish_interval)
except KeyboardInterrupt:
    print("Simulation terminated")
    client.disconnect()