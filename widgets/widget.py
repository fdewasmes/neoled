#!/usr/bin/env python

from PIL import Image
from PIL import ImageDraw
from rgbmatrix import graphics
import operator
import logging

logger = logging.getLogger('neoled')

def color_tweaker(f):
    ops = {
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '=': operator.eq
    }

    def wrapped(self, *args, **kwargs):
        # observer is of the form :
        # ["observed_property_name", "color_chooser", "impacted_property_name"]
        # color_chooser is of the form:
        # ["operator", "compared_to_value", "resulting_color"]
        for observer in self.observe:
            if observer[0] == f.__name__:

                if len(self.color_choosers) > observer[1]:

                    g = filter(None,
                               map(lambda color_chooser: (
                                   color_chooser[2] if ops[color_chooser[0]](args[0], type(args[0])(
                                       color_chooser[1])) else None),
                                   self.color_choosers[observer[1]]))

                    if len(g) > 0:
                        
                        setattr(self, observer[2], g[0])

        r = f(self, *args, **kwargs)
        return r

    return wrapped

class Widget(object):
    """ Base class for all widgets """

    def __init__(self, matrix, bus, imageCanvas, x, y, width, height):
        """ constructor
        Parameters
        ----------
        matrix
            the led matrix as returned by RGB Matrix
        bus
            the instance of the cyrusbus used thourghout the program
        imageCanvas
            the canvas on which we will write
        x: int
            x position of the widget
        y: int
            y position of the widget
        width: int
            width of the widget
        height: int
            height of the widget"""
        self._matrix = matrix
        self._bus = bus
        self._imageCanvas = imageCanvas
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def bus(self):
        return self._bus

    @bus.setter
    def bus(self, value):
        self._bus = value

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, value):
        self._matrix = value

    @property
    def imageCanvas(self):
        return self._imageCanvas

    @imageCanvas.setter
    def imageCanvas(self, value):
        self._imageCanvas = value

    def color_from_hex(self, c):
        r = (c >> 16) & 0xFF
        g = (c >> 8) & 0xFF
        b = c & 0xFF
        return graphics.Color(r, g, b)

    def drawBorder(self, color):
        #if color.red == color.green == color.blue == 0:
        #    return
        draw = ImageDraw.Draw(self.imageCanvas)
        draw.rectangle((self.x, self.y, self.x + self.width - 1, self.y - self.height + 1), outline=color)
        del draw

    def drawBackground(self, color):
        #if color.red == color.green == color.blue == 0:
        #    return
        draw = ImageDraw.Draw(self.imageCanvas)
        draw.rectangle((self.x, self.y, self.x + self.width - 1, self.y - self.height + 1), fill=color, outline="#000000")
        del draw
