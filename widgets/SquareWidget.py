#!/usr/bin/env python

from widget import Widget
from widget import color_tweaker
import logging

logger = logging.getLogger('neoled')


class SquareWidget(Widget):
    def callback(self, bus, argument):
        self.called_bus = bus
        self.val = argument

    def __init__(self, matrix, bus, imageCanvas, x=0, y=0, width=4, height=4, color="#FF0000",
                 borderColor="#0A0A0A", listen="event.key", color_choosers={}, observe=[], type=__name__):
        super(SquareWidget, self).__init__(matrix, bus, imageCanvas, x, y, width, height)
        self._color = color
        self.borderColor = borderColor
        self._val = 0
        self.color_choosers = color_choosers
        self.observe = observe
        self.bus.subscribe(listen, self.callback)
        logger.info("Started Square Widget at x: " + str(self.x) + " y: " + str(self.y))

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def val(self):
        return self._val

    @val.setter
    @color_tweaker
    def val(self, value):
        self._val = value

    def Display(self):
        super(SquareWidget, self).drawBackground(self.color)
        super(SquareWidget, self).drawBorder(self.borderColor)
