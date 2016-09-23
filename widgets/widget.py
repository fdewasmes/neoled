#!/usr/bin/env python


from rgbmatrix import graphics
import time


class Widget(object):
    """ Base class for all widgets """

    def __init__(self, matrix, bus, offscreenCanvas, x, y, width, height):
        """ constructor
        Parameters
        ----------
        matrix
            the led matrix as returned by RGB Matrix
        bus
            the instance of the cyrusbus used thourghout the program
        offscreenCanvas
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
        self._offscreenCanvas = offscreenCanvas
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
    def offscreenCanvas(self):
        return self._offscreenCanvas

    @offscreenCanvas.setter
    def offscreenCanvas(self, value):
        self._offscreenCanvas = value

    def color_from_hex(self, c):
        r = (c >> 16) & 0xFF
        g = (c >> 8) & 0xFF
        b = c & 0xFF
        return graphics.Color(r, g, b)

    def drawBorder(self, color):
        if color.red == color.green == color.blue == 0:
            return
        graphics.DrawLine(self.offscreenCanvas, self.x, self.y, self.x + self.width, self.y, color)
        graphics.DrawLine(self.offscreenCanvas, self.x + self.width, self.y, self.x + self.width, self.y - self.height,
                          color)
        graphics.DrawLine(self.offscreenCanvas, self.x, self.y, self.x, self.y - self.height, color)
        graphics.DrawLine(self.offscreenCanvas, self.x, self.y - self.height, self.x + self.width, self.y - self.height,
                          color)

    def drawBackground(self, color):
        if color.red == color.green == color.blue == 0:
            return
        for i in range(1, self.width):
            for j in range(1, self.height):
                self.offscreenCanvas.SetPixel(self.x + i, self.y - j, color.red, color.green, color.blue)
