from client import connect_mqtt


class Analyser:

    def __init__(self):
        print("analyser : initialising")
        self.client = connect_mqtt("analyser")
    
    def start(self, qos: int, delay: int, instance_count: int):
        print("analyser : publishing request values...")
        self.client.loop_start()
        self.client.publish(topic="request/qos", payload=qos, qos=2)
        self.client.publish(topic="request/delay", payload=delay, qos=2)
        self.client.publish(topic="request/instancecount", payload=instance_count, qos=2)
        self.client.loop_stop()