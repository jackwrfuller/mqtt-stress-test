from client import connect_mqtt
from time import time
from statistics import median

class Listener:

    

    def __init__(self, csv_writer):
        print("listener : initialising")
        self.client = connect_mqtt("listener")
        self.count = 0
        self.out_order_count = 0
        self.last_pub_value = [0, 0, 0, 0, 0]
        self.last_recv = [0, 0, 0, 0, 0]
        self.intermessage_gap_1 = [0]
        self.intermessage_gap_2 = [0]
        self.intermessage_gap_3 = [0]
        self.intermessage_gap_4 = [0]
        self.intermessage_gap_5 = [0]
        
        self.writer = csv_writer

        self.delay = 0
        self.qos = 0
        self.instancecount = 0

    def listen(self, qos: int, delay: int, instancecount: int):
        def on_message(client, userdata, msg):
            #print(f" listener : received {msg.payload.decode()} from {msg.topic} topic")
            topic = msg.topic
            time_recv = time()
            value = int(msg.payload.decode())

            self.count += 1
            # update pub counter
            pub_index = int(topic[12]) - 1
            self.check_out_order(pub_index, value)
            self.last_pub_value[pub_index] = self.last_pub_value[pub_index] + 1
            #self.update_intermessage_gap(pub_index, time_recv, value)
        
        self.delay = delay
        self.qos = qos
        self.instancecount = instancecount

        self.client.subscribe(f"counter/pub-1/{qos}/{delay}")
        self.client.subscribe(f"counter/pub-2/{qos}/{delay}")
        self.client.subscribe(f"counter/pub-3/{qos}/{delay}")
        self.client.subscribe(f"counter/pub-4/{qos}/{delay}")
        self.client.subscribe(f"counter/pub-5/{qos}/{delay}")

        self.client.on_message = on_message
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()

    def check_out_order(self, pub_index: int, value: int):
        last_val = self.last_pub_value[pub_index]
        if last_val > value:
            self.out_order_count += 1

    def update_intermessage_gap(self, pub_index: int, time_recv: float, value: int):
        gap = time_recv - self.last_recv[pub_index]
        self.last_recv[pub_index] = time_recv

        # Check messages were consecutive
        if value is not self.last_pub_value[pub_index] + 1:
            return

        if pub_index == 0:
            self.intermessage_gap_1.append(gap)
        elif pub_index == 1:
            self.intermessage_gap_2.append(gap)
        elif pub_index == 2:
            self.intermessage_gap_3.append(gap)
        elif pub_index == 3:
            self.intermessage_gap_4.append(gap)
        else:
            self.intermessage_gap_5.append(gap)
    
    def get_stats(self):
        if self.delay == 0:
            loss_rate = 0
        else:
            loss_rate = ( self.count ) / ( 60000 / self.delay ) 
        avg_messages = self.count / 60
        out_order_rate = self.out_order_count / self.count
        median_gaps = (median(self.intermessage_gap_1), median(self.intermessage_gap_2), median(self.intermessage_gap_3), 
                       median(self.intermessage_gap_4), median(self.intermessage_gap_5))
        self.writer.writerow([self.qos, self.delay, self.instancecount, avg_messages, loss_rate, 
                             out_order_rate, median_gaps[0], median_gaps[1], median_gaps[2], median_gaps[3], median_gaps[4]])