#!/usr/bin/env python
from PIL import Image
from PIL import ImageDraw
from widget import Widget
from collections import deque
import logging

logger = logging.getLogger('neoled')


class GraphWidget(Widget):
    def callback(self, bus, argument):
        self.called_bus = bus
        self.data.append(argument)
        self.data.popleft()

    def __init__(self, matrix, bus, imageCanvas, x=0, y=10, width=50, height=10, lineColor="#FFFFFF",
                 borderColor="#0A0A0A", bgColor="#00000A", listen="event.key",
                 ranges=[], barWidth=2, stacked=True,
                 type=__name__):
        super(GraphWidget, self).__init__(matrix, bus, imageCanvas, x, y, width, height)
        self.lineColor = lineColor
        self.borderColor = borderColor
        self.bgColor = bgColor

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
        logger.info(self.data)
        if (m > 0):
            scale = self.height * 1.0 / m

        self.scale = scale

        count = 0
        draw = ImageDraw.Draw(self.imageCanvas)
        for d in list(self.data):
            
            if self.stacked:
                for r in self.ranges:
                    if (r[0] <= d ):
                        color = r[2]
                        top = min([d,r[1]])
                        #logger.info("color:"+color+" d:"+str(d)+" r[0]:"+str(r[0])+" r[1]:"+str(r[1])+" top:"+str(top))

                        x1 = self.x+count * self.bar_width
                        y1 = int(round(self.y-r[0]*scale))
                        x2 = self.x+(count+1)*self.bar_width
                        y2 = int(round(self.y - top*self.scale))
                        #logger.info("x1:"+str(x1)+" y1:"+str(y1)+" x2:"+str(x2)+" y2:"+str(y2))
                        draw.rectangle([(x1,y1),(x2,y2)], fill=color)
            else:
                for r in self.ranges:
                    if ((r[0] <= d) and (d < r[1]) ):
                        color = r[2]
                        break
                x1 = self.x+count * self.bar_width
                y1 = self.y
                x2 = self.x+(count+1)*self.bar_width
                y2 = int(round(self.y - d*self.scale))

                draw.rectangle([(x1,y1),(x2,y2)], fill=color)
            count += 1

        del draw
        super(GraphWidget, self).drawBorder(self.borderColor)
