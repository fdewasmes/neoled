#!/usr/bin/env python

from widget import Widget
from collections import deque
import logging

logger = logging.getLogger('neoled')


class GraphWidget(Widget):
    def callback(self, bus, argument):
        self.called_bus = bus
        self.data.append(argument)
        self.data.popleft()

    def __init__(self, matrix, bus, offscreenCanvas, x=0, y=10, width=50, height=10, lineColor="0xFFFFFF",
                 borderColor="0x0A0A0A", bgColor="0x00000A", listen="event.key",
                 ranges=[(0, 3, "0x00FF00"), (3, 5, "0xFF8800"), (5, 10, "0xFF0000")], barWidth=2, stacked=True,
                 type=__name__):
        super(GraphWidget, self).__init__(matrix, bus, offscreenCanvas, x, y, width, height)
        self.lineColor = super(GraphWidget, self).color_from_hex(int(lineColor, 0))
        self.borderColor = super(GraphWidget, self).color_from_hex(int(borderColor, 0))
        self.bgColor = super(GraphWidget, self).color_from_hex(int(bgColor, 0))

        self.bus.subscribe(listen, self.callback)

        self.ranges = ranges
        self.bar_width = barWidth
        self.stacked = stacked
        self.data = deque([0] * (self.width // self.bar_width))
        self.scale = 1.0
        logger.info("Started Graph Widget at x: " + str(self.x) + " y: " + str(self.y))

    def Display(self):

        super(GraphWidget, self).drawBackground(self.bgColor)

        m = max(list(self.data))
        scale = 1.0
        
        if (m > 0):
            scale = self.height * 1.0 / m

        if scale < self.scale:
            self.scale = scale

        count = 0
        for d in list(self.data):

            for i in range(0, self.height, 1):
                color = super(GraphWidget, self).color_from_hex(0x000000)

                for r in self.ranges:
                    if self.stacked:
                        if (i < d * scale) and (r[0] <= i < r[1]):
                            color = super(GraphWidget, self).color_from_hex(int(r[2], 0))
                    else:
                        if (i < d * scale) and (r[0] <= d < r[1]):
                            color = super(GraphWidget, self).color_from_hex(int(r[2], 0))

                for w in range(self.bar_width):
                    # print "d: "+str(d)+"w:" + str(w) + " count:" + str(count) + " = " + str(self.x + w + (count * self.bar_width))
                    self.offscreenCanvas.SetPixel(self.x + w + (count * self.bar_width), self.y - i, color.red,
                                                  color.green, color.blue)

            count += 1

        super(GraphWidget, self).drawBorder(self.borderColor)
