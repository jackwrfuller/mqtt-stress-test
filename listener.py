from client import connect_mqtt
from time import time


class Listener:

    def __init__(self, csv_writer):
        print("listener : initialising")
        self.client = connect_mqtt("listener")
        self.count = 0
        self.writer = csv_writer

    def listen(self, qos: int, delay: int):
        def on_message(client, userdata, msg):
            print(f" listener : received {msg.payload.decode()} from {msg.topic} topic")
            self.writer.writerow([str(msg.topic), str(time()), str(msg.payload.decode())])
            self.count += 1

        self.client.subscribe(f"counter/pub-1/{qos}/{delay}")
        self.client.subscribe(f"counter/pub-2/{qos}/{delay}")
        self.client.subscribe(f"counter/pub-3/{qos}/{delay}")
        self.client.subscribe(f"counter/pub-4/{qos}/{delay}")
        self.client.subscribe(f"counter/pub-5/{qos}/{delay}")

        self.client.on_message = on_message

        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
