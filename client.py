from paho.mqtt import client as mqtt_client

host = 'pi.jackwrfuller.au'
port = 2883


def connect_mqtt(name: str) -> mqtt_client:
    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print(name, ": Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", reason_code)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.connect(host, port)
    return client
