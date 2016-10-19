import time

class DatetimeProvider(object):
    def __init__(self, bus, emit="event.key", refreshInterval=1, type=__name__):
        self.bus = bus
        self.emit = emit
        self.refreshInterval = refreshInterval

    def run(self):
        self.bus.publish(self.emit, argument=time.strftime("%H:%M:%S", time.localtime()))

    def shutdown(self):
        None
        # do nothing
