#!/usr/bin/env python
# Display a runtext with double-buffering.
from PIL import Image, ImageDraw, ImageFont
from widget import Widget
from widget import color_tweaker
from rgbmatrix import graphics
import textwrap
import logging
from jsonpath_rw import jsonpath, parse
import os

logger = logging.getLogger('neoled')
dir_path = os.path.dirname(os.path.realpath(__file__))


class TextWidget(Widget):
    def callback(self, bus, argument):
        self.called_bus = bus
        self._value = argument

    def jsonp(self, bus, path="", query="", body=None):
        self.called_bus = bus

        if self.jsonpath_expr is not None:
            matches = self.jsonpath_expr.find(body)
            if len(matches) > 0:
                self.text = str(matches[0].value)

    def __init__(self, matrix, bus, imageCanvas, x=0, y=10, width=50, height=10, defaultText="{}",
                 font="6x10.bdf", textColor="#FFFFFF", borderColor="#000", bgColor="#000",
                 listen=None, color_choosers={}, observe=[], jsonpath=None, type=__name__):
        super(TextWidget, self).__init__(matrix, bus, imageCanvas, x, y, width, height)
        self._value = "None"
        self._text = defaultText
        self._load_font(dir_path + "/../matrix/fonts/" + font)

        self._color = textColor
        self.borderColor = borderColor
        self._bgColor = bgColor


        if listen is not None:
            self.bus.subscribe(listen, self.callback)
        if jsonpath is not None:
            self.bus.subscribe(jsonpath[0], self.jsonp)
            if jsonpath[1] is not None:
                self.jsonpath_expr = parse(jsonpath[1])
            else:
                self.jsonpath_expr = None

        self.color_choosers = color_choosers
        self.observe = observe

        logger.info("Started Text Widget at x: " + str(self.x) + " y: " + str(self.y))


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

    @property
    def text(self):
        return self._text.format(self._value)

    @text.setter
    @color_tweaker
    def text(self, value):
        self._text = value

    def _load_font(self, font):
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf", 13, encoding="unic")

        self.chw, self.chh = self.font.getsize("A")
        self.max_char_per_line = (self.width - 2) // self.chw
        self.max_line = (self.height - 2) // self.chh

    def Display(self):

        super(TextWidget, self).drawBackground(self.bgColor)

        # avoid drawing text if it's too tall
        if (self.chh > self.height):
            return

        # crop text if it's too long
        tmptext = self.text[0:self.max_char_per_line * self.max_line]
        wrapped = textwrap.fill(tmptext, self.max_char_per_line)

        draw = ImageDraw.Draw(self.imageCanvas)
        draw.text((self.x + 1, self.y - self.height), wrapped, self.color, self.font)
        del draw
        super(TextWidget, self).drawBorder(self.borderColor)
