#!/usr/bin/env python

from widget import Widget
from rgbmatrix import graphics
from cyrusbus import Bus


class BidibulleWidget(Widget):
    def callback(self, bus, argument):
        self.called_bus = bus
        if argument in self.bidibulles:
            self.current = argument
            self.animOffset = 0

    def __init__(self, matrix, bus, offscreenCanvas, x=100, y=10, width=5, height=5, color="0xFFFFFF", borderColor="0",
                 bgColor="0", listen="event.key", bidibulle='default', zoom=1, type=__name__):
        super(BidibulleWidget, self).__init__(matrix, bus, offscreenCanvas, x, y, width, height)
        self.color = super(BidibulleWidget, self).color_from_hex(int(color, 0))
        self.borderColor = super(BidibulleWidget, self).color_from_hex(int(borderColor, 0))
        self.bgColor = super(BidibulleWidget, self).color_from_hex(int(bgColor, 0))
        self.bidibulles = {'default': 0x1FFFFFF, 'fabrice': 0x11757EA, 'axel': 0x1B5555B, 'yvan': 0x0EAFDD5}
        self.bus.subscribe(listen, self.callback)
        self.current = bidibulle
        self.zoom = zoom
        self.animOffset = 0

    def Display(self):

        super(BidibulleWidget, self).drawBackground(self.bgColor)
        offset = 0
        if (self.bgColor.red > 0) or (self.bgColor.green > 0) or (self.bgColor.blue > 0):
            offset = 1
        bb = self.bidibulles[self.current]
        if self.animOffset < self.height:
            self.animOffset += 1
        for i in range(0, 25):
            mask = 1 << i
            row = i // 5
            column = i % 5
            if bb & mask:
                for yy in range(self.zoom):
                    for z in range(self.zoom):
                        self.offscreenCanvas.SetPixel(self.x + (5 * self.zoom) - column * self.zoom - z,
                                                      self.y - row * self.zoom - yy - offset + (
                                                      self.height - self.animOffset), self.color.red, self.color.green,
                                                      self.color.blue)
            else:
                for yy in range(self.zoom):
                    for z in range(self.zoom):
                        self.offscreenCanvas.SetPixel(self.x + (5 * self.zoom) - column * self.zoom - z,
                                                      self.y - row * self.zoom - yy - offset + (
                                                      self.height - self.animOffset), self.bgColor.red,
                                                      self.bgColor.green, self.bgColor.blue)
        super(BidibulleWidget, self).drawBorder(self.borderColor)
