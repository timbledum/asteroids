import pyxel

from ship import Ship
from asteroid import Asteroid
import constants


class Game:
    def __init__(self):

        pyxel.init(200, 200, scale=2)
        self.ship = Ship(*constants.SHIP_INITIAL_POSITION, constants.SHIP_COLOUR)
        Asteroid.initiate_game()

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.ship.accelerate()
        if pyxel.btnp(pyxel.KEY_SPACE, 0, 4):
            self.ship.shoot()

        if pyxel.btn(pyxel.KEY_LEFT):
            self.ship.rotate("l")
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.ship.rotate("r")
        elif pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.ship.update_position()
        Asteroid.update_all()

    def check_collisions(self):
        pass

    def draw(self):
        pyxel.cls(constants.BACKGROUND_COLOUR)
        self.ship.display()
        Asteroid.display_all()
        

if __name__ == "__main__":
    Game()