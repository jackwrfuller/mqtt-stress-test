import random

from paho.mqtt import client as mqtt_client
from time import sleep


host = 'localhost'
port = 1883
topics = ["request/qos", "request/delay", "request/instancecount"]
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'

qos = None
delay = None
instance_count = None

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", reason_code)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(host, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global qos, delay, instance_count
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if msg.topic == "request/qos":
            print("Setting QOS")
            qos = msg.payload.decode()
        if msg.topic == "request/delay":
            print("Setting delay")
            delay = msg.payload.decode()    
        if msg.topic == "request/instancecount":
            print("Setting instance count")
            instance_count = msg.payload.decode()        
    for topic in topics:
        print("Subscribing to ", topic)
        client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    while (qos is None) or (delay is None) or (instance_count is None):
        sleep(1)
        print("Waiting for config to be set")
    client.loop_stop()
    print("Config set!")


if __name__ == '__main__':
    run()






