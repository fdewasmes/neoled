#!/usr/bin/env python

from widget import Widget
from widget import color_tweaker


class BidibulleWidget(Widget):
    bidibulles = {
        'default': 0x1FFFFFF,
        'fabrice': 0x11757EA,
        'axel': 0x1B5555B,
        'yvan': 0x0EAFDD5,
        'david': 0x0BF3BD8,
        'antoine': 0x0EDB9D5,
        'jc': 0x1FAFDDB,
        'nicolas': 0x0477DD5,
        'florian': 0xEDFBEE

    }

    def callback(self, bus, argument):
        self.called_bus = bus
        if argument in BidibulleWidget.bidibulles:
            self.current = argument
            self.anim_offset = 0

    def __init__(self, matrix, bus, offscreenCanvas, x=100, y=10, width=5, height=5, color="0xFFFFFF", borderColor="0",
                 bgColor="0", listen="event.key", bidibulle='default', zoom=1, color_choosers={}, observe=[],
                 type=__name__):
        super(BidibulleWidget, self).__init__(matrix, bus, offscreenCanvas, x, y, width, height)
        self._color = super(BidibulleWidget, self).color_from_hex(int(color, 0))
        self.borderColor = super(BidibulleWidget, self).color_from_hex(int(borderColor, 0))
        self._bgColor = super(BidibulleWidget, self).color_from_hex(int(bgColor, 0))

        self._current = bidibulle
        self.zoom = zoom
        self.anim_offset = 0
        self.color_choosers = color_choosers

        self.observe = observe

        self.bus.subscribe(listen, self.callback)

    @property
    def current(self):
        return self._current

    @current.setter
    @color_tweaker
    def current(self, value):
        self._current = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def bgColor(self):
        return self._bgColor

    @bgColor.setter
    def bgColor(self, value):
        self._bgColor = value

    def Display(self):

        # super(BidibulleWidget, self).drawBackground(self.bgColor)

        # avoid painting on the border if it's present
        border_offset = 0
        if (self.borderColor.red > 0) or (self.borderColor.green > 0) or (self.borderColor.blue > 0):
            border_offset = 1
        bb = BidibulleWidget.bidibulles[self.current]

        # clear the widget canvas in case we start or restart animation from scratch.
        # This happens when the widget to be displayed changes
        if self.anim_offset == 0:
            for w in range(self.width):
                for h in range(self.height):
                    self.offscreenCanvas.SetPixel(self.x + w,
                                                  self.y - h, self.bgColor.red,
                                                  self.bgColor.green, self.bgColor.blue)

        # start painting the bidibulle
        for i in range(0, 25):
            mask = 1 << i
            row = i // 5
            column = i % 5
            if bb & mask:
                for yy in range(self.zoom):
                    for z in range(self.zoom):
                        self.offscreenCanvas.SetPixel(self.x + (5 * self.zoom) - column * self.zoom - z,
                                                      self.y - row * self.zoom - yy - border_offset + (
                                                          self.zoom * 5 - self.anim_offset), self.color.red,
                                                      self.color.green,
                                                      self.color.blue)
            else:
                for yy in range(self.zoom):
                    for z in range(self.zoom):
                        self.offscreenCanvas.SetPixel(self.x + (5 * self.zoom) - column * self.zoom - z,
                                                      self.y - row * self.zoom - yy - border_offset + (
                                                          self.zoom * 5 - self.anim_offset), self.bgColor.red,
                                                      self.bgColor.green, self.bgColor.blue)

        # draw border
        super(BidibulleWidget, self).drawBorder(self.borderColor)

        # increment animation step
        if self.anim_offset < self.height:
            self.anim_offset += self.zoom
            self.anim_offset = min(self.anim_offset, self.zoom * 5)
