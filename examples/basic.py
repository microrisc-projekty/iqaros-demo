import paho.mqtt.client as mqtt
import json
from datetime import datetime


# Broker config
BROKER_HOST = "192.168.1.2" # Your IP address
BROKER_PORT = 1883
RESPONSE_TOPIC = "gateway/12345/iqrf/responses" # Your response topic

# BROKER_USER = "admin"
# BROKER_PASSWORD = "admin"


def handle_message(msg: str):
    response = json.loads(msg)

    # Only proceed if reading has finished
    if response["data"]["rsp"]["reading"] == False:

        devices = response["data"]["rsp"]["devices"]

        current_time = datetime.now()
        print(f"\n\nNew message: (at {current_time})\n")

        # The message contains data from all devices
        for dev in devices:
            print(f"Address: {dev['address']}:")

            # Each device can have multiple sensors
            for sensor in dev["sensors"]:
                if sensor["value"] is None:
                    continue
                  
                print(
                    f"  {sensor['name']}: {round(sensor['value'], 2)} {sensor['unit']}"
                )


# paho-mqtt download and documentation: https://pypi.org/project/paho-mqtt/
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# client.username_pw_set(BROKER_USER, BROKER_PASSWORD) # Only when using authentication


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT broker")

    # Subscribe to your gateways Response topic
    client.subscribe(RESPONSE_TOPIC)


def on_message(client, userdata, msg):
    # Parse JSON
    handle_message(msg.payload.decode())


client.on_connect = on_connect
client.on_message = on_message


client.connect(BROKER_HOST, BROKER_PORT, 60)

client.loop_forever()
