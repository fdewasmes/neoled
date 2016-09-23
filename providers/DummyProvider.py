import random


class DummyProvider(object):
    def __init__(self, bus, emit="event.key", refreshInterval=1, type=__name__):
        self.bus = bus
        self.emit = emit
        self.refreshInterval = refreshInterval

    def run(self):
        a = random.randint(0, 10)
        self.bus.publish(self.emit, argument=a)
