from publisher import Publisher
from analyser import Analyser
from listener import Listener
import threading
from time import time
import csv

publisher_threads = list()


def run():
    results = open("test.csv", 'w', newline='')
    writer = csv.writer(results)
    fields = ["topic", "time", "value"]
    writer.writerow(fields)

    for qos in range(3):
        for delay in range(5):
            for instancecount in range(1, 6):
                analyser = Analyser()
                listener = Listener(writer)
                launch_publishers(number=5)
                analyser.start(qos, delay, instancecount)
                listener.listen(qos, delay)
                for thread in publisher_threads:
                    thread.join()
                listener.stop()
                analyser.client.disconnect()
                listener.client.disconnet()

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
    client.disconnect()


def report_stats(results):
    return


if __name__ == '__main__':
    run()
