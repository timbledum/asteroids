import math

import pyxel

SHIP_POINTS = [(0,-4), (2, 2), (-2, 2)]
ROTATION = 0.1

class ShipPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rotate_around_point(self, radians):
        """Rotate the point around the origin.

        Taken from https://ls3.io/post/rotate_a_2d_coordinate_around_a_point_in_python/"""
        x, y = self.x, self.y
        self.x = x * math.cos(radians) + y * math.sin(radians)
        self.y = -x * math.sin(radians) + y * math.cos(radians)



class Ship:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y

        self.points = []
        for point in SHIP_POINTS:
            self.points.append(ShipPoint(*point))

    def rotate(self, direction):
        if direction = "l":
            multipler = 1
        elif direction = "r":
            multipler = -1
        else:
            raise ValueError("Direction must be the 'l'eft or 'r'ight")

        for point in self.points:
            point.rotate_around_point(ROTATION * mutliplier)

    def display()


