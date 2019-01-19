"""The game of asteroids in pyxel.

## To dos ##
- [X] Somehow fix asteroids spawning to not place on player
- [x] Player death
- [ ] Player death animation
- [x] Scoring
- [-] Lives
- [x] Get asteroids spawning (accelerating)
- [ ] Sound effects
- [ ] Music
- [ ] High score system
- [ ] Reset system working

"""

import pyxel

from ship import Ship
from bullet import Bullet
from asteroid import Asteroid
import constants
import collisions
from utils import center_text


class Game:
    def __init__(self):

        pyxel.init(200, 200, scale=2)
        self.ship = Ship(*constants.SHIP_INITIAL_POSITION, constants.SHIP_COLOUR)
        Asteroid.init_class(self.ship)
        Asteroid.initiate_game()

        self.colission = False
        self.next_spawn = self.spawn_speed = constants.INITIAL_SPAWN_FREQUENCY
        self.death = False

        pyxel.run(self.update, self.draw)

    def update(self):
        self.check_input()

        Bullet.update_all()
        Asteroid.update_all()

        if not self.death:
            self.ship.update_position()
            self.check_spawn_asteroid()
            self.check_collisions()


    def check_input(self):
        if not self.death:
            if pyxel.btn(pyxel.KEY_UP):
                self.ship.accelerate()
            if pyxel.btnp(pyxel.KEY_SPACE, 0, constants.BULLET_SHOOT_FREQUENCY):
                self.ship.shoot()

            if pyxel.btn(pyxel.KEY_LEFT):
                self.ship.rotate("l")
            elif pyxel.btn(pyxel.KEY_RIGHT):
                self.ship.rotate("r")
        elif pyxel.btnp(pyxel.KEY_R):
            pass #Reset ship and asteroids

        if pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()


    def check_collisions(self):
        if collisions.detect_ship_asteroid_colissions(self.ship, Asteroid):
            self.ship.destroy()
            self.death = True
            self.colission = True
        else:
            self.colission = False

        collisions.detect_bullet_asetoid_colissions(Bullet, Asteroid)

    def check_spawn_asteroid(self):
        if pyxel.frame_count >= self.next_spawn:
            Asteroid()
            self.next_spawn += self.spawn_speed
            self.spawn_speed += constants.SPAWN_FREQUENCY_MOVEMENT

    def draw(self):
        background_colour = constants.BACKGROUND_COLOUR if not self.death else constants.DEATH_COLOUR
        
        pyxel.cls(background_colour)
        Bullet.display_all()
        Asteroid.display_all()
        if not self.death:
            self.ship.display()
            self.draw_score()
        else:
            self.draw_death()

        

    def draw_score(self):
        """Draw the score at the top."""

        score = "{:04}".format(Asteroid.asteroid_score)
        pyxel.text(3, 3, score, constants.SCORE_COLOUR)
        pyxel.text(3, 15, str(self.spawn_speed), constants.SCORE_COLOUR)
        pyxel.text(3, 27, str(pyxel.frame_count), constants.SCORE_COLOUR)


    def draw_death(self):
        """Draw a blank screen with some text."""
        display_text = ["YOU DIED"]
        display_text.append("Your score is {:04}".format(Asteroid.asteroid_score))
        #display_text.append("YOU HAVE A NEW HIGH SCORE!")

        text_area_height = len(display_text) * (pyxel.constants.FONT_HEIGHT + 2) - 2
        pyxel.rect(0, constants.DEATH_HEIGHT - 2, pyxel.width, constants.DEATH_HEIGHT + text_area_height, constants.DEATH_STRIP_COLOUR)

        for i, text in enumerate(display_text):
            y_offset = (pyxel.constants.FONT_HEIGHT + 2) * i
            text_x = center_text(text, pyxel.width,pyxel.constants.FONT_WIDTH)
            pyxel.text(text_x, constants.DEATH_HEIGHT + y_offset, text, constants.DEATH_TEXT_COLOUR)


if __name__ == "__main__":
    Game()
