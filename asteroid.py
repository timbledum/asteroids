import math
import random

import pyxel

ASTEROID_ROTATION = 0.1
INITIAL_QUANTITY = 3



class Asteroid:
    asteroids = []

    def __init__(self):
        self.x = random.randint(0, pyxel.width)
        self.y = randonm.randint(0, pyxel.height)
        self.spin_direction = random.choice((-1, 1))

    def update(self):
        pass
        # Rotate the asteroid

    def destroy(self):
        pass

    def display(self):
        pass
        # Similar to ship
    
    @staticmethod
    def initiate_game():
        for i in range(INITIAL_QUANTITY):
            Asteroid()

    @staticmethod
    def update_all():
        for asteroid in Asteroid.asteroids:
            asteroid.update()


    @staticmethod
    def display_all():
        for asteroid in Asteroid.asteroids:
            asteroid.display()
