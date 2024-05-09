from publisher import Publisher
def run():
    p = Publisher("pub-1")
    p.subscribe()
    p.publish()
    p.reset()
    p.subscribe()

if __name__ == '__main__':
    run()
