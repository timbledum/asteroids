import math
import random

import pyxel

from utils import check_bounds, rotate_around_origin, Point
import constants


class Asteroid:
    asteroids = []

    def __init__(self):
        self.x = random.randint(0, pyxel.width)
        self.y = random.randint(0, pyxel.height)
        self.colour = constants.ASTEROID_COLOUR

        self.direction = random.random() * math.pi * 2
        # Need to add this to initial state

        self.spin_direction = random.choice((-1, 1))

        self.points = []
        for point in constants.ASTEROID_SHAPES:
            self.points.append(Point(*point))

        Asteroid.asteroids.append(self)

    def update(self):

        rotation_angle = constants.ASTEROID_ROTATION * self.spin_direction

        for point in self.points:
            point.rotate_point(rotation_angle)
        # Rotate the asteroid

        self.x = check_bounds(self.x, pyxel.width, constants.BUFFER)
        self.y = check_bounds(self.y, pyxel.height, constants.BUFFER)

    def destroy(self):
        pass

    def display(self):
        for point1, point2 in zip(self.points, self.points[1:] + [self.points[0]]):
            pyxel.line(
                x1=point1.x + self.x,
                y1=point1.y + self.y,
                x2=point2.x + self.x,
                y2=point2.y + self.y,
                col=self.colour,
            )

    @staticmethod
    def initiate_game():
        for i in range(constants.ASTEROID_INITIAL_QUANTITY):
            Asteroid()

    @staticmethod
    def update_all():
        for asteroid in Asteroid.asteroids:
            asteroid.update()

    @staticmethod
    def display_all():
        for asteroid in Asteroid.asteroids:
            asteroid.display()
