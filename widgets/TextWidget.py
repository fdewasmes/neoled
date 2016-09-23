#!/usr/bin/env python
# Display a runtext with double-buffering.
from widget import Widget
from rgbmatrix import graphics
from cyrusbus import Bus
import time
import sched


class TextWidget(Widget):
    def callback(self, bus, argument):
        self.called_bus = bus
        self.text = argument

    def __init__(self, matrix, bus, offscreenCanvas, x=0, y=10, width=50, height=10, defaultText="hello",
                 font="matrix/fonts/6x10.bdf", textColor="0xFFFFFF", borderColor="0x0A0A0A", bgColor="0x00000A",
                 listen="event.key", type=__name__):
        super(TextWidget, self).__init__(matrix, bus, offscreenCanvas, x, y, width, height)
        self.text = defaultText
        self._load_font(font)

        self.color = super(TextWidget, self).color_from_hex(int(textColor, 0))
        self.borderColor = super(TextWidget, self).color_from_hex(int(borderColor, 0))
        self.bgColor = super(TextWidget, self).color_from_hex(int(bgColor, 0))

        self.bus.subscribe(listen, self.callback)

    def _load_font(self, font):
        self.font = graphics.Font()
        self.font.LoadFont(font)
        self.chw = self.font.CharacterWidth(ord('a'))
        self.maxchar = self.width // self.chw

    def Display(self):
        # self.offscreenCanvas.Clear()
        super(TextWidget, self).drawBorder(self.borderColor)
        super(TextWidget, self).drawBackground(self.bgColor)

        # avoid drawing text if it's too tall
        if (self.font.height > self.height):
            return

        # graphics.DrawText(self.offscreenCanvas, self.font, self.x+len, self.y, self.color, str(len))
        # for i in range(10):
        #    self.offscreenCanvas.SetPixel(self.x+i, self.y-1,0,0,0)

        # crop text if it's too long
        self.text = self.text[0:self.maxchar]
        len = graphics.DrawText(self.offscreenCanvas, self.font, self.x, self.y, self.color, self.text)
