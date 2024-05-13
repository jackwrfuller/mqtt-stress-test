from publisher import Publisher, TEST_TIME
from analyser import Analyser
import threading
import time



publisher_threads = list()

def run():
    analyser = Analyser()

    for qos in range(3):
        for delay in range(1000,1001):
            for instancecount in range(1, 6):
                launch_publishers(number=5)
                # wait to ensure clients are given a chance to initialise and connect
                # TODO replace with event
                time.sleep(2)
                analyser.start(qos, delay, instancecount)
                for thread in publisher_threads:
                    thread.join()
                print("DONE")
    
    
def launch_publishers(number: int):
        for thread_index in range(number):
            thread = threading.Thread(target=publisher_loop, args=(thread_index + 1,))
            thread.start()
            publisher_threads.append(thread)


def publisher_loop(number: int):
        client_name = number
        client = Publisher(client_name)
        client.subscribe()
        client.publish()
        # client.reset()
        # client.subscribe()
        

if __name__ == '__main__':
    run()
