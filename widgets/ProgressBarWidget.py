#!/usr/bin/env python

from widget import Widget
from widget import color_tweaker
import math
import logging

logger = logging.getLogger('neoled')


class ProgressBarWidget(Widget):
    def callback(self, bus, argument):
        self.called_bus = bus
        self.progress = argument

    def __init__(self, matrix, bus, offscreenCanvas, x=0, y=10, width=50, height=10, color="0xFF0000",
                 borderColor="0x0A0A0A", bgColor="0x00000A", listen="event.key", progress=0, color_choosers={},
                 observe=[], type=__name__):
        super(ProgressBarWidget, self).__init__(matrix, bus, offscreenCanvas, x, y, width, height)
        self._color = super(ProgressBarWidget, self).color_from_hex(int(color, 0))
        self.borderColor = super(ProgressBarWidget, self).color_from_hex(int(borderColor, 0))
        self.bgColor = super(ProgressBarWidget, self).color_from_hex(int(bgColor, 0))
        self._progress = progress
        self.color_choosers = color_choosers
        self.observe = observe
        self.bus.subscribe(listen, self.callback)
        logger.info("Started ProgessBar Widget at x: " + str(self.x) + " y: " + str(self.y))

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def progress(self):
        return self._progress

    @progress.setter
    @color_tweaker
    def progress(self, value):
        self._progress = value

    def Display(self):
        super(ProgressBarWidget, self).drawBackground(self.bgColor)
        super(ProgressBarWidget, self).drawBorder(self.borderColor)


        for h in range(self.y, self.y - self.height, -1):
            for w in range(0, int(math.floor(self.width * self.progress))):
                self.offscreenCanvas.SetPixel(self.x + w, h, self.color.red, self.color.green, self.color.blue)
