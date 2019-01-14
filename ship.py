import math

import pyxel

SHIP_POINTS = [(0, -8), (4, 4), (0, 2), (-4, 4)]
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
        self.colour = colour

        self.points = []
        for point in SHIP_POINTS:
            self.points.append(ShipPoint(*point))

    def rotate(self, direction):
        if direction == "l":
            multipler = 1
        elif direction == "r":
            multipler = -1
        else:
            raise ValueError("Direction must be the 'l'eft or 'r'ight")

        for point in self.points:
            point.rotate_around_point(ROTATION * multipler)

    def display(self):
        """Display lines between each point."""
        for point1, point2 in zip(self.points, self.points[1:] + [self.points[0]]):
            pyxel.line(
                x1=point1.x + self.x,
                y1=point1.y + self.y,
                x2=point2.x + self.x,
                y2=point2.y + self.y,
                col=self.colour,
            )
