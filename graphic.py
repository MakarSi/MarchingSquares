import numpy as np
import math
from random import random
from abc import ABC, ABCMeta


def blend(color, alpha, base=None):
    # Конвертировать цвет в шестнадцатеричный

    if base is None:
        base = [255, 255, 255]
    out = [int(round((alpha * color[i]) + ((1 - alpha) * base[i]))) for i in range(3)]

    return ''.join(["%02x" % e for e in out])


class Graphic2D(metaclass=ABCMeta):
    def draw(self, canvas, **kwargs):
        raise NotImplementedError


class Shape2D(ABC, Graphic2D):
    def __init__(self, x, y, rotation=float(0)):
        self._center = np.array([x, y])
        self._rotation = rotation
        self._item = None

    def get_center(self):
        return np.copy(self._center)

    def set_center(self, x, y):
        self._center = np.array([x, y])

    def get_item(self):
        return self._item


class Rectangle(Shape2D):
    def __init__(self, x, y, width, height):
        super(Rectangle, self).__init__(x, y)
        self._width = width
        self._height = height

    def get_center(self):
        return self._center

    def get_width(self):
        return self._width

    def set_width(self, width):
        self._width = width

    def get_height(self):
        return self._height

    def set_height(self, height):
        self._height = height

    def draw(self, canvas, **kwargs):
        if not self._item:
            x = self._center[0]
            y = self._center[1]
            width = self._width / 2
            height = self._height / 2
            x1 = x - width
            x2 = x + width
            y1 = y - height
            y2 = y + height
            self._item = canvas.create_rectangle(x1, y1, x2, y2, **kwargs)


class Segment(Shape2D):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.vector = self.end - self.start
        center = self.start + self.vector / 2
        super(Segment, self).__init__(center[0], center[1])
        dx = self.end[0] - self.start[0]
        dy = self.end[1] - self.start[1]
        if math.isclose(dx, 0):
            self.A = 1
            self.B = 0
            self.C = start[0]
        else:
            self.A = dy / dx
            self.B = -1
            self.C = self.A * self.start[0] + self.B * self.start[1]
        assert math.isclose(self.A * self.start[0] + self.B * self.start[1] - self.C, 0)

    def draw(self, canvas, **kwargs):
        if not self._item:
            x1, y1 = self.start[0], self.start[1]
            x2, y2 = self.end[0], self.end[1]
            self._item = canvas.create_line(x1, y1, x2, y2, **kwargs)

    def x(self, y):
        dy = self.end[1] - self.start[1]
        if math.isclose(dy, 0):
            return random.random() * (self.end[0] - self.start[0]) + self.start[0]
        return (self.C - self.B * y) / self.A

    def y(self, x):
        dx = self.end[0] - self.start[0]
        if math.isclose(dx, 0):
            return random.random() * (self.end[1] - self.start[1]) + self.start[1]
        return (self.C - self.A * x) / self.B

    # point = start + (end - start) * t
    def t(self, point):
        x, y = point
        dx = self.end[0] - self.start[0]
        dy = self.end[1] - self.start[1]
        tx = (x - self.start[0]) / dx if not math.isclose(dx, 0) else 0
        ty = (y - self.start[1]) / dy if not math.isclose(dy, 0) else 0
        return tx, ty
