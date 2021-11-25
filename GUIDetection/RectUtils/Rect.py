from .Point import  *

class Rect:

    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def tl(self):
        return (int(self.x), int(self.y))

    def tl_Pt(self):
        return Point(int(self.x), int(self.y))

    def br_Pt(self):
        return Point(int(self.x + self.width), int(self.y + self.height))

    def br(self):
        return (int(self.x + self.width), int(self.y + self.height))

    def reshape(self, x, y, width, height):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        return self

    def area(self):
        return self.height * self.width