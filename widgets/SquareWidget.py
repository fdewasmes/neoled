#!/usr/bin/env python

from widget import Widget
import math
from widget import color_tweaker


class SquareWidget(Widget):
    def callback(self, bus, argument):
        self.called_bus = bus
        self.val = argument

    def __init__(self, matrix, bus, offscreenCanvas, x=0, y=0, width=4, height=4, color="0xFF0000",
                 borderColor="0x0A0A0A", listen="event.key", color_choosers={}, observe=[], type=__name__):
        super(SquareWidget, self).__init__(matrix, bus, offscreenCanvas, x, y, width, height)
        self._color = super(SquareWidget, self).color_from_hex(int(color, 0))
        self.borderColor = super(SquareWidget, self).color_from_hex(int(borderColor, 0))
        self._val = 0
        self.color_choosers = color_choosers
        self.observe = observe
        self.bus.subscribe(listen, self.callback)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        print "color " + value
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
