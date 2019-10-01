import math


class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, new):
        self.x += new.x
        self.y += new.y

    def add_vect(self, new):
        return Vec2d(self.x + new.x, self.y + new.y)

    def sub(self, new):
        self.x -= new.x
        self.y -= new.y

    def sub_vect(self, new):
        return Vec2d(self.x - new.x, self.y - new.y)

    def angle(self):
        return math.atan2(-self.y,self.x)

    def limit(self, max_):
        if self.mag() > max_:
            self.set_mag(max_)

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def set_mag(self, value):
        self.x, self.y = value*self.x/self.mag(), value*self.y/self.mag()

    def distance(self, new):
        return math.sqrt((self.x - new.x) * (self.x - new.x) + (self.y - new.y) * (self.y - new.y))

