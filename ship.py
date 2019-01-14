import math

import pyxel

SHIP_POINTS = [(0, -8), (4, 4), (0, 2), (-4, 4)]
ROTATION = 0.1
ACCELERATION = 1
DRAG = 0.96


def rotate_around_origin(xy, radians):
    """Rotate the point around the origin.

    Taken from https://ls3.io/post/rotate_a_2d_coordinate_around_a_point_in_python/"""
    x, y = xy
    xx = x * math.cos(radians) + y * math.sin(radians)
    yy = -x * math.sin(radians) + y * math.cos(radians)
    return xx, yy

class ShipPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rotate_point(self, radians):
        """Rotate the point around the origin."""
        self.x, self.y = rotate_around_origin((self.x, self.y), radians)


class Ship:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour
        self.direction = 0
        self.momentum_x = 0
        self.momentum_y = 0

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

        rotation_angle = ROTATION * multipler

        for point in self.points:
            point.rotate_point(rotation_angle)
            
        self.direction += rotation_angle

    def accelerate(self):
        acc_x, acc_y = rotate_around_origin((0, -ACCELERATION), self.direction)
        self.momentum_x += acc_x
        self.momentum_y += acc_y


    def update_position(self):
        self.x += self.momentum_x
        self.y += self.momentum_y
        self.momentum_x *= DRAG
        self.momentum_y *= DRAG

        if self.x < 0:
            self.x = pyxel.width
        if self.x > pyxel.width:
            self.x = 0
        if self.y < 0:
            self.y = pyxel.height
        if self.y > pyxel.height:
            self.y = 0



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
