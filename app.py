from publisher import Publisher
from analyser import Analyser
from listener import Listener
import threading
from time import time, sleep
import csv

publisher_threads = list()



def run():
    results = open("test.csv", 'a', newline='')
    writer = csv.writer(results)

    for qos in range(3):
        for delay in range(5):
            for instancecount in range(1, 6):
                print(f"starting test {qos}/{delay}/{instancecount}")
                analyser = Analyser()
                listener = Listener(writer)
                launch_publishers(number=5)
                analyser.start(qos, delay, instancecount)
                listener.listen(qos, delay, instancecount)
                for thread in publisher_threads:
                    thread.join()
                listener.stop()
                analyser.client.disconnect()
                listener.client.disconnect()
                sleep(5)
                listener.get_stats()
                print(f"ending test {qos}/{delay}/{instancecount}")
                sleep(5) 

    results.close()
    print(f"Listener counted {listener.count}")
    report_stats(results)


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
    #client.disconnect()


def report_stats(results):
    return


if __name__ == '__main__':
    run()
