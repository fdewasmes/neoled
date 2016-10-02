#!/usr/bin/python
import os
import time
from phue import Bridge
import os
import logging

logger = logging.getLogger('neoled')

dir_path = os.path.dirname(os.path.realpath(__file__))

class HueCommand():
    def callback(self, bus, hue=0, brightness=100, saturation=25):
        self.called_bus = bus
        logger.info("setting lights to hue: " + str(hue) + " brightness: " + str(brightness) + " saturation: " + str(
            saturation))
        for light in self.lightbulbs:
            self.lights[light].on = True
            self.lights[light].hue = hue
            self.lights[light].brightness = brightness
            self.lights[light].saturation = saturation

    def __init__(self, bus, listen="hue.command", bridgeIp="192.168.136.56", config_file_path="./confighue",
                 type=__name__, lightbulbs=[]):
        self.bus = bus
        self.listen = listen
        self.lightbulbs = lightbulbs
        self.bus.subscribe(self.listen, self.callback)

        self.b = Bridge(bridgeIp, config_file_path=config_file_path)
        self.b.connect()
        self.b.get_api()
        self.lights = self.b.get_light_objects('name')
        logger.debug(self.lights)
