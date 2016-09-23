#!/usr/bin/env python

from widget import Widget
from rgbmatrix import graphics
from cyrusbus import Bus
import time
import sched
from collections import deque


class GraphWidget(Widget):
    def callback(self, bus, argument):
        self.called_bus = bus
        self.data.append(argument)
        self.data.popleft()

    def __init__(self, matrix, bus, offscreenCanvas, x=0, y=10, width=50, height=10, lineColor="0xFFFFFF",
                 borderColor="0x0A0A0A", bgColor="0x00000A", listen="event.key", type=__name__):
        super(GraphWidget, self).__init__(matrix, bus, offscreenCanvas, x, y, width, height)
        self.lineColor = super(GraphWidget, self).color_from_hex(int(lineColor, 0))
        self.borderColor = super(GraphWidget, self).color_from_hex(int(borderColor, 0))
        self.bgColor = super(GraphWidget, self).color_from_hex(int(bgColor, 0))

        self.bus.subscribe(listen, self.callback)
        self.data = deque([0] * (self.width // 2))

    def Display(self):

        super(GraphWidget, self).drawBorder(self.borderColor)
        super(GraphWidget, self).drawBackground(self.bgColor)

        # graphics.DrawText(self.offscreenCanvas, self.font, self.x+len, self.y, self.color, str(len))
        # for i in range(10):
        #    self.offscreenCanvas.SetPixel(self.x+i, self.y-1,0,0,0)

        # crop text if it's too long
        count = 0
        for d in list(self.data):
            for i in range(0, d, 1):
                r = 255
                g = 255
                b = 255
                if 0 <= d <= 5:
                    r = 0
                    g = 255
                    b = 0
                elif 6 <= d <= 8:
                    r = 255
                    g = 128
                    b = 0
                else:
                    r = 255
                    g = 0
                    b = 0
                self.offscreenCanvas.SetPixel(self.x + count * 2, self.y - i, r, g, b)
                self.offscreenCanvas.SetPixel(self.x + 1 + count * 2, self.y - i, r, g, b)
            count += 1
