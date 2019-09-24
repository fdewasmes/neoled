#!/usr/bin/env python

from widget import Widget
from widget import color_tweaker
from PIL import Image


class ImageWidget(Widget):
    def callback(self, bus, argument):
        self.called_bus = bus

    def __init__(self, matrix, bus, imageCanvas, x=0, y=0, width=128, height=32, borderColor="#000000",
                 bgColor="#000000", listen="event.key", imagePath=None,
                 type=__name__):
        super(ImageWidget, self).__init__(matrix, bus, imageCanvas, x, y, width, height)

        self.borderColor = borderColor
        self._bgColor = bgColor
        self.image_path = imagePath

        self.bus.subscribe(listen, self.callback)

    @property
    def bgColor(self):
        return self._bgColor

    @bgColor.setter
    def bgColor(self, value):
        self._bgColor = value

    def Display(self):
        if self.image_path is None:
            return
        self.image = Image.open(self.image_path)
        self.image.resize((self.width, self.height), Image.ANTIALIAS)
        self.imageCanvas.paste(self.image, (self.x, self.y - self.height))
