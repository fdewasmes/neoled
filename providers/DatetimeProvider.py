import subprocess


class DatetimeProvider(object):
    def __init__(self, bus, emit="event.key", refreshInterval=1, type=__name__):
        self.bus = bus
        self.emit = emit
        self.refreshInterval = refreshInterval

    def run(self):
        parser.bus.publish(self.emit, argument=strftime("%H:%M:%S", gmtime()))
