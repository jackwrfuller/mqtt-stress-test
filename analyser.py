from client import connect_mqtt
from time import sleep

class Analyser:

    def __init__(self):
        print("analyser : initialising")
        self.client = connect_mqtt("analyser")
        
    
        self.list_of_dicts = []
    
    def start(self, qos: int, delay: int, instance_count: int):
        def on_message(client, userdata, msg):
            print(f" analyser : received `{msg.payload.decode()}` from `{msg.topic}` topic")
            self.list_of_dicts.append({"instance": "pub-1", "qos":qos, "delay":delay, "value": msg.payload.decode()})
        
        print("analyser : publishing request values...")
        self.client.loop_start()
        self.client.publish(topic="request/qos", payload=qos, qos=2)
        self.client.publish(topic="request/delay", payload=delay, qos=2)
        self.client.publish(topic="request/instancecount", payload=instance_count, qos=2)
        
        print("analyser : listening to counter topic")
        self.client.subscribe(f"counter/pub-1/`{qos}`/`{delay}`")
        self.client.subscribe(f"counter/pub-2/`{qos}`/`{delay}`")
        self.client.subscribe(f"counter/pub-3/`{qos}`/`{delay}`")
        self.client.subscribe(f"counter/pub-4/`{qos}`/`{delay}`")
        self.client.subscribe(f"counter/pub-5/`{qos}`/`{delay}`")
        self.client.on_message = on_message

        sleep(5)
        
        self.client.loop_stop()
        
        print(self.list_of_dicts)
    
        