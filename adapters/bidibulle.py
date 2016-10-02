#!/usr/bin/env python
import logging

logger = logging.getLogger('neoled')


class BidibulleAdapter(object):
    def callback(self, bus, path="", query="", body=""):
        logger.info("Received Bidibulle query : " + query)
        logger.debug("PATH :" + path)
        logger.debug("QUERY :" + query)
        logger.debug("BODY :" + str(body))
        self.adapt(path, query)

    def __init__(self, bus, listen="web.bidibulle", emit="bidibulle.event", type=__name__):
        self.bus = bus
        self.emit = emit
        self.listen = listen
        self.bus.subscribe(self.listen, self.callback)

    def adapt(self, path, query):
        paths = path.split("/")

        self.bus.publish(self.emit, argument=paths[-1])
