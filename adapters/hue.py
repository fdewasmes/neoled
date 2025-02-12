#!/usr/bin/env python

from cyrusbus import Bus
import urlparse
import logging

logger = logging.getLogger('neoled')

class HueAdapter(object):
    def callback(self, bus, path="", query="", body=""):
        logger.debug("PATH :" + path)
        logger.debug("QUERY :" + query)
        logger.debug("BODY :" + str(body))
        self.adapt(path, query)

    def __init__(self, bus, listen="web.hue", emit="hue.command", type=__name__):
        self.bus = bus
        self.emit = emit
        self.listen = listen
        self.bus.subscribe(self.listen, self.callback)

    def adapt(self, path, query):

        query_string = urlparse.parse_qsl(query)
        d = dict(query_string)

        hue = None
        brightness = None
        saturation = None
        if "hue" in d:
            hue = int(d["hue"])
        if "brightness" in d:
            brightness = int(d["brightness"])
        if "saturation" in d:
            saturation = int(d["saturation"])
        if hue is not None:
            self.bus.publish(self.emit, hue=hue, brightness=brightness, saturation=saturation)
