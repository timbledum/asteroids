import math

import pyxel

from bullet import Bullet
from utils import check_bounds, rotate_around_origin, Point

SHIP_POINTS = [(0, -8), (4, 4), (0, 2), (-4, 4)]
ROTATION = 0.1
ACCELERATION = 0.4
MAX_ACCELERATION = 6
DRAG = 0.98
BUFFER = 7

BULLET_COLOUR = 11
BULLET_VELOCITY = 5






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
            self.points.append(Point(*point))

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

        acceleration = math.hypot(self.momentum_x, self.momentum_y)
        if acceleration > MAX_ACCELERATION:
            scale = MAX_ACCELERATION / acceleration
            self.momentum_x *= scale
            self.momentum_y *= scale
            assert round(math.hypot(self.momentum_x, self.momentum_y), 0) == MAX_ACCELERATION


    def shoot(self):
        vel_x, vel_y = rotate_around_origin((0, -BULLET_VELOCITY), self.direction)
        ship_tip = self.points[0]
        Bullet(self.points[0].x + self.x, self.points[0].y + self.y, vel_x, vel_y, BULLET_COLOUR)


    def update_position(self):
        self.x += self.momentum_x
        self.y += self.momentum_y
        self.momentum_x *= DRAG
        self.momentum_y *= DRAG

        self.x = check_bounds(self.x, pyxel.width, BUFFER)
        self.y = check_bounds(self.y, pyxel.height, BUFFER)

        Bullet.update_all()


    def display(self):
        """Display lines between each point."""
        Bullet.display_all()

        for point1, point2 in zip(self.points, self.points[1:] + [self.points[0]]):
            pyxel.line(
                x1=point1.x + self.x,
                y1=point1.y + self.y,
                x2=point2.x + self.x,
                y2=point2.y + self.y,
                col=self.colour,
            )


