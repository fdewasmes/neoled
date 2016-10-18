import random


class RandomProvider(object):
    def __init__(self, bus, emit="event.key", refreshInterval=1, lowerBound=0, upperBound=10, type=__name__):
        self.bus = bus
        self.emit = emit
        self.refreshInterval = refreshInterval
        self.lower_bound = lowerBound
        self.upper_bound = upperBound

    def run(self):
        a = random.randint(self.lower_bound, self.upper_bound)
        self.bus.publish(self.emit, argument=a)

    def shutdown(self):
        None
        # do nothing
