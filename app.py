from publisher import Publisher
from analyser import Analyser
import threading
import time

publisher_threads = list()

def run():
    launch_publishers(number=5)
    analyser = Analyser()
    analyser.start(1, 1000, 3)
    
    
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
        client.reset()
        client.subscribe()
        

if __name__ == '__main__':
    run()
