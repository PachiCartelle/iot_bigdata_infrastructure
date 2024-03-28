import paho.mqtt.client as mqtt
import json

# This function is a callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code: {str(rc)}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("office/+")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # Decode JSON payload
    message = json.loads(msg.payload)
    print(f"Sensor Message: {message}")

# Create an MQTT client instance
client = mqtt.Client()

# Assign the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
print("Connecting to broker")
client.loop_forever()