"""The game of asteroids in pyxel.

## To dos ##
- [ ] Somehow fix asteroids spawning to not place on player
- [ ] Player death
- [ ] Player death animation
- [ ] Scoring
- [ ] Lives
- [ ] Get asteroids spawning (accelerating)
- [ ] Sound effects
- [ ] Music

"""

import pyxel

from ship import Ship
from bullet import Bullet
from asteroid import Asteroid
import constants
import collisions


class Game:
    def __init__(self):

        pyxel.init(200, 200, scale=2)
        self.ship = Ship(*constants.SHIP_INITIAL_POSITION, constants.SHIP_COLOUR)
        Asteroid.init_class(self.ship)
        Asteroid.initiate_game()
        self.colission = False
        pyxel.run(self.update, self.draw)

    def update(self):
        self.check_input()

        Bullet.update_all()
        self.ship.update_position()
        Asteroid.update_all()
        self.check_collisions()

    def check_input(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.ship.accelerate()
        if pyxel.btnp(pyxel.KEY_SPACE, 0, 4):
            self.ship.shoot()

        if pyxel.btn(pyxel.KEY_A):
            Asteroid()

        if pyxel.btn(pyxel.KEY_LEFT):
            self.ship.rotate("l")
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.ship.rotate("r")
        elif pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

    def check_collisions(self):
        if collisions.detect_ship_asteroid_colissions(self.ship, Asteroid):
            self.ship.destroy()
            self.colission = True
        else:
            self.colission = False

        collisions.detect_bullet_asetoid_colissions(Bullet, Asteroid)

    def draw(self):
        pyxel.cls(constants.BACKGROUND_COLOUR + self.colission)
        Bullet.display_all()
        Asteroid.display_all()
        self.ship.display()


if __name__ == "__main__":
    Game()
