from paho.mqtt import client as mqtt_client
import time
from client import connect_mqtt

class Publisher:

    topics = ["request/qos", "request/delay", "request/instancecount"]

    def __init__(self, name):
        self.name = name
        self.qos = None
        self.delay = None
        self.instance_count = None
        # Connect to MQTT brokers
        self.client = connect_mqtt(name)


    def subscribe(self):
        def on_message(client, userdata, msg):
            print(self.name, f": received `{msg.payload.decode()}` from `{msg.topic}` topic")
            if msg.topic == "request/qos":
                print(self.name,": setting QOS")
                self.qos = int(msg.payload.decode())
            if msg.topic == "request/delay":
                print(self.name,": setting delay")
                self.delay = int(msg.payload.decode())
            if msg.topic == "request/instancecount":
                print(self.name, ": setting instance count")
                self.instance_count = msg.payload.decode()

        for topic in self.topics:
            print(self.name, ": subscribing to ", topic)
            self.client.subscribe(topic)
        self.client.on_message = on_message

        self.client.loop_start()
        while (self.qos is None) or (self.delay is None) or (self.instance_count is None):
            time.sleep(0.1)
        self.client.loop_stop()
        print(self.name, ": config set")

    def publish(self):
        topic = f"counter/`{self.name}`/`{self.qos}`/`{self.delay}`"

        time_end = time.time() + 60
        counter = 0
        print(self.name, ": beginning stress test")
        while time.time() < time_end:
            self.client.publish(topic, payload=counter, qos=self.qos)
            counter += 1
            time.sleep(self.delay / 1000)
        print(self.name, ": end stress test")
        
    def reset(self):
        self.qos = None
        self.delay = None
        self.instance_count = None


