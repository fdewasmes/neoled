#!/usr/bin/env python

from cyrusbus import Bus
import urlparse


class BidibulleAdapter(object):
    def callback(self, bus, path="", query="", body=""):
        print "PATH :" + path
        print "QUERY :" + query
        print "BODY :" + str(body)
        self.adapt(path, query)

    def __init__(self, bus, listen="web.bidibulle", emit="bidibulle.event", type=__name__):
        self.bus = bus
        self.emit = emit
        self.listen = listen
        self.bus.subscribe(self.listen, self.callback)

    def adapt(self, path, query):
        query_string = urlparse.parse_qsl(query)
        d = dict(query_string)
        print "parsed query : " + str(d)

        if "bidibulle" in d:
            self.bus.publish(self.emit, argument=d["bidibulle"])
