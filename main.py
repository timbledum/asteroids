import pyxel

from ship import Ship

SHIP_COLOUR = 14
SHIP_INITIAL_POSITION = (100, 100)
BACKGROUND_COLOUR = 13


class Game:
    def __init__(self):

        pyxel.init(200, 200, scale=2)
        self.ship = Ship(*SHIP_INITIAL_POSITION, SHIP_COLOUR)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.ship.accelerate()
        if pyxel.btnp(pyxel.KEY_SPACE, 0, 5):
            self.ship.shoot()

        if pyxel.btn(pyxel.KEY_LEFT):
            self.ship.rotate("l")
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.ship.rotate("r")
        elif pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.ship.update_position()

    def draw(self):
        pyxel.cls(BACKGROUND_COLOUR)
        self.ship.display()

if __name__ == "__main__":
    Game()