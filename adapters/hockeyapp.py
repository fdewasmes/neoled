#!/usr/bin/env python


import logging

logger = logging.getLogger('neoled')

class HockeyAppAdapter(object):
    def callback(self, bus, path="", query="", body=""):
        logger.debug("PATH :" + path)
        logger.debug("QUERY :" + query)
        logger.debug("BODY :" + str(body))
        self.adapt(path, query, body)

    def __init__(self, bus, listen="web.hockey", emit="hockey.event", type=__name__):
        self.bus = bus
        self.emit = emit
        self.listen = listen
        self.bus.subscribe(self.listen, self.callback)

    def adapt(self, path, query, body):
        if body["type"] == "crash_reason":
            reason = body["crash_reason"]["reason"]
            self.bus.publish(self.emit, argument=reason)
