#!/usr/bin/env python
from PIL import Image, ImageDraw, ImageFont
from widget import Widget
from widget import color_tweaker
import math
import logging

logger = logging.getLogger('neoled')


class ProgressBarWidget(Widget):
    def callback(self, bus, argument):
        self.called_bus = bus
        self.progress = argument

    def __init__(self, matrix, bus, imageCanvas, x=0, y=10, width=50, height=10, color="#FF0000",
                 borderColor="#0A0A0A", bgColor="#00000A", listen="event.key", progress=0, color_choosers={},
                 observe=[], type=__name__):
        super(ProgressBarWidget, self).__init__(matrix, bus, imageCanvas, x, y, width, height)
        self._color = color
        self.borderColor = borderColor
        self.bgColor = bgColor
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


        draw = ImageDraw.Draw(self.imageCanvas)
        draw.rectangle((self.x, self.y , self.x+int(math.floor(self.width * self.progress)), self.y- self.height+1), fill=self.color, )
        super(ProgressBarWidget, self).drawBorder(self.borderColor)
