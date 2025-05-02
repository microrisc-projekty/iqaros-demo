import paho.mqtt.client as mqtt
import json
from datetime import datetime
from typing import List

# Broker config
BROKER_HOST = "10.0.0.186"
BROKER_PORT = 1883
BROKER_USER = "admin"
BROKER_PASSWORD = "admin"
RESPONSE_TOPIC = "gateway/02426da6df1e5780/iqrf/responses"


class Measurement:
    address: int
    name: str
    unit: str
    value: float
    timestamp: int


# We can store the measured data in an array
measurements: List[Measurement] = []


# And later compute the average
def get_average(sensor_name: str):
    sum = 0
    count = 0

    for m in measurements:
        if m.name == sensor_name and not m.value is None:
            sum += m.value
            count += 1

    return sum / count


def handle_message(msg: str):
    # Parse JSON
    response = json.loads(msg)

    # Only proceed if reading has finished
    if response["data"]["rsp"]["reading"] == False:

        devices = response["data"]["rsp"]["devices"]

        current_time = datetime.now()

        # The message contains data from all devices
        for dev in devices:
            # Each device can have multiple sensors
            for sensor in dev["sensors"]:
                m = Measurement()
                m.address = dev["address"]
                m.name = sensor["name"]
                m.unit = sensor["unit"]
                m.value = sensor["value"]
                m.timestamp = current_time.timestamp()

                measurements.append(m)

        print(
            f"{current_time}> Average temperature is {round(get_average('Temperature'), 2)} °C, average humidity is {round(get_average('Relative humidity'), 2)} %"
        )


# paho-mqtt download and documentation: https://pypi.org/project/paho-mqtt/
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(BROKER_USER, BROKER_PASSWORD)


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT broker")

    # Subscribe to your gateways Response topic
    client.subscribe(RESPONSE_TOPIC)


def on_message(client, userdata, msg):
    handle_message(msg.payload.decode())


client.on_connect = on_connect
client.on_message = on_message


client.connect(BROKER_HOST, BROKER_PORT, 60)

client.loop_forever()
