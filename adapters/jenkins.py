#!/usr/bin/env python

from cyrusbus import Bus
import urlparse


class JenkinsAdapter(object):
    def callback(self, bus, path, query):
        self.adapt(path, query)

    def __init__(self, bus, listen="web.jenkins", emit='jenkins.event', type=__name__):
        self.bus = bus
        self.emit = emit
        self.listen = listen
        self.bus.subscribe(self.listen, self.callback)

    def adapt(self, path, query):
        query_string = urlparse.parse_qsl(query)
        d = dict(query_string)

        if "test" in query_string:
            num = int(query_string["test"][0])

        self.bus.publish(self.emit, argument=path)
