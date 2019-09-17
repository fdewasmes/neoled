import subprocess
import logging

logger = logging.getLogger('neoled')
class ShellProvider(object):
    def __init__(self, bus, emit="event.key", refreshInterval=1, shell_command="/usr/games/fortune -s", type=__name__):
        self.bus = bus
        self.emit = emit
        self.refreshInterval = refreshInterval
        self.command = shell_command

    def run(self):
        outb = subprocess.Popen(self.command, stdout=subprocess.PIPE, shell=True, executable="/bin/bash").communicate()[
            0]

        out = outb[:-1].decode('ascii')
        #logger.info(out)
        self.bus.publish(self.emit, argument=out)

    def shutdown(self):
        None
        # do nothing
