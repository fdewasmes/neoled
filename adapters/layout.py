#!/usr/bin/env python

from cyrusbus import Bus
import urlparse


class LayoutAdapter(object):
    def callback(self, bus, path="", query="", body=""):
        print "PATH :" + path
        print "QUERY :" + query
        print "BODY :" + str(body)
        self.adapt(path, query)

    def __init__(self, bus, listen="web.layout", emit="layout.event", type=__name__):
        self.bus = bus
        self.emit = emit
        self.listen = listen
        self.bus.subscribe(self.listen, self.callback)

    def adapt(self, path, query):
        paths = path.split("/")

        self.bus.publish(self.emit, argument=paths[-1])
