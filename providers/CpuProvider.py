import subprocess


class CpuProvider(object):
    def __init__(self, bus, emit="event.key", refreshInterval=1, type=__name__):
        self.bus = bus
        self.emit = emit
        self.refreshInterval = refreshInterval

    def run(self):
        command = 'top -bn1 | grep "Cpu(s)" | sed "s/.*, *\\([0-9.]*\\)%* id.*/\\1/" | awk \'{print 100 - $1"%"}\''
        cpub = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, executable="/bin/bash").communicate()[0]
        # t = subprocess.getoutput('./getcpu.sh')
        cpu = cpub[:-1].decode('ascii')
        self.bus.publish(self.emit, argument=cpu)

    def shutdown(self):
        None
        # do nothing
