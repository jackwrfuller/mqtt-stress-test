from paho.mqtt import client as mqtt_client
import time


# noinspection SpellCheckingInspection
class Publisher:
    host = 'pi.jackwrfuller.au'
    port = 2883
    topics = ["request/qos", "request/delay", "request/instancecount"]

    def __init__(self, name):
        self.name = name
        self.qos = None
        self.delay = None
        self.instance_count = None

        # Connect to MQTT broker
        self.client = self.connect_mqtt()

    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, reason_code, properties):
            if reason_code == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", reason_code)

        client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2)
        # client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(self.host, self.port)
        return client

    def subscribe(self):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            if msg.topic == "request/qos":
                print("Setting QOS")
                self.qos = int(msg.payload.decode())
            if msg.topic == "request/delay":
                print("Setting delay")
                self.delay = int(msg.payload.decode())
            if msg.topic == "request/instancecount":
                print("Setting instance count")
                self.instance_count = msg.payload.decode()

        for topic in self.topics:
            print("Subscribing to ", topic)
            self.client.subscribe(topic)
        self.client.on_message = on_message

        self.client.loop_start()
        while (self.qos is None) or (self.delay is None) or (self.instance_count is None):
            time.sleep(0.1)
        self.client.loop_stop()
        print("Config set!")

    def publish(self):
        topic = f"counter/`{self.name}`/`{self.qos}`/`{self.delay}`"

        time_end = time.time() + 60
        counter = 0
        while time.time() < time_end:
            self.client.publish(topic, payload=counter, qos=self.qos)
            counter += 1
            time.sleep(self.delay / 1000)

    def reset(self):
        self.qos = None
        self.delay = None
        self.instance_count = None


