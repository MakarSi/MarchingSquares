from graphic import Rectangle


class Node:
    def __init__(self, index=None):
        self._index = index
        self._contents = []
        self._leaves = []

    def contents(self):
        return self._contents

    def leaves(self):
        return self._leaves


class Quadrant(Node, Rectangle):
    def __init__(self, x, y, width, height, index=None):
        Node.__init__(self, index=index)
        Rectangle.__init__(self, x, y, width, height)
        self.canvas = None

    def draw(self, canvas, fill="", outline="black"):
        super(Quadrant, self).draw(canvas, fill=fill, outline=outline)
