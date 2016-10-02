import random


class RollingCounterProvider(object):
    def __init__(self, bus, emit="event.key", refreshInterval=1, lowerBound=0, upperBound=10, step=1, type=__name__):
        self.bus = bus
        self.emit = emit
        self.refreshInterval = refreshInterval
        self.lower_bound = lowerBound
        self.upper_bound = upperBound
        self.current = self.lower_bound
        self.step = step

    def run(self):
        self.current = self.current + self.step
        if self.current < self.lower_bound:
            self.current = self.upper_bound
        if self.current > self.upper_bound:
            self.current = self.lower_bound
        self.bus.publish(self.emit, argument=self.current)
