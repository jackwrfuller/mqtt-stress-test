from publisher import Publisher
from analyser import Analyser
from listener import Listener
import threading
import time

publisher_threads = list()

qos = 1
delay = 1000
instancecount = 2

def run():
    analyser = Analyser()
    listener = Listener()


    launch_publishers(number=5)

    analyser.start(qos, delay, instancecount)
    listener.listen(qos, delay)


    for thread in publisher_threads:
        thread.join()
    listener.stop()

    print(f"Listener counted {listener.count}")



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


if __name__ == '__main__':
    run()
