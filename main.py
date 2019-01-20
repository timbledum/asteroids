"""The game of asteroids in pyxel.

## To dos ##
- [X] Somehow fix asteroids spawning to not place on player
- [x] Player death
- [ ] Player death animation [still want to refine]
- [x] Scoring
- [-] Lives
- [x] Get asteroids spawning (accelerating)
- [x] Sound effects
- [ ] Music
- [x] High score system (persisting to disk)
- [x] Reset system working
- [x] Get flame on ship on acceleration
- [ ] Tidy up and document

"""

import pyxel

from ship import Ship, ShipBreakup
from bullet import Bullet
from asteroid import Asteroid
import constants
import collisions
from utils import center_text, get_highscore, save_highscore
import sound


class Game:
    def __init__(self):

        pyxel.init(200, 200, scale=2)
        self.ship = Ship(*constants.SHIP_INITIAL_POSITION, constants.SHIP_COLOUR)
        Asteroid.init_class(self.ship)
        sound.init_music()

        self.reset_game()
        self.high_score = get_highscore(constants.HIGH_SCORE_FILE)

        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.ship.reset()
        Asteroid.initiate_game()
        self.death = False
        self.spawn_speed = constants.INITIAL_SPAWN_FREQUENCY
        self.next_spawn = pyxel.frame_count + self.spawn_speed

    def update(self):
        self.check_input()

        Bullet.update_all()
        Asteroid.update_all()

        if not self.death:
            self.ship.update_position()
            self.check_spawn_asteroid()
            self.check_collisions()
        else:
            self.ship_breakup.update()

    def check_input(self):
        if not self.death:
            if pyxel.btn(pyxel.KEY_UP):
                if not self.ship.accelerating:
                    sound.start_accelerate()
                self.ship.accelerate()
            else:
                if self.ship.accelerating:
                    sound.stop_accelerate()
                self.ship.accelerating = False

            if pyxel.btnp(pyxel.KEY_SPACE, 0, constants.BULLET_SHOOT_FREQUENCY):
                self.ship.shoot()

            if pyxel.btn(pyxel.KEY_SPACE):
                self.ship.yes_shoot()
            else:
                self.ship.no_shoot()

            if pyxel.btn(pyxel.KEY_LEFT):
                self.ship.rotate("l")
            elif pyxel.btn(pyxel.KEY_RIGHT):
                self.ship.rotate("r")
        elif pyxel.btnp(pyxel.KEY_R):
            self.reset_game()

        if pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

    def check_collisions(self):
        if collisions.detect_ship_asteroid_colissions(self.ship, Asteroid):
            self.death_event()

        collisions.detect_bullet_asetoid_colissions(Bullet, Asteroid)

    def death_event(self):
        self.ship.destroy()
        self.ship_breakup = ShipBreakup(self.ship)
        self.death = True
        sound.death()

        if Asteroid.asteroid_score > self.high_score:
            self.high_score = Asteroid.asteroid_score
            save_highscore(constants.HIGH_SCORE_FILE, self.high_score)

    def check_spawn_asteroid(self):
        if pyxel.frame_count >= self.next_spawn:
            Asteroid()
            self.next_spawn += self.spawn_speed
            self.spawn_speed *= constants.SPAWN_FREQUENCY_MOVEMENT
            sound.spawn()

    def draw(self):
        background_colour = (
            constants.BACKGROUND_COLOUR if not self.death else constants.DEATH_COLOUR
        )

        pyxel.cls(background_colour)
        Bullet.display_all()
        Asteroid.display_all()
        if not self.death:
            self.ship.display()
            self.draw_score()
        else:
            self.draw_death()
            self.ship_breakup.display()

    def draw_score(self):
        """Draw the score at the top."""

        score = "{:04}".format(Asteroid.asteroid_score)
        high_score = "HS:{:04}".format(self.high_score)
        high_score_x = pyxel.width - 2 - (7 * pyxel.constants.FONT_WIDTH)

        pyxel.text(3, 3, score, constants.SCORE_COLOUR)
        pyxel.text(high_score_x, 3, high_score, constants.SCORE_COLOUR)
        pyxel.text(3, 15, str(self.spawn_speed), constants.SCORE_COLOUR)
        pyxel.text(3, 27, str(pyxel.frame_count), constants.SCORE_COLOUR)

    def draw_death(self):
        """Draw a blank screen with some text."""
        display_text = ["YOU DIED"]
        display_text.append("Your score is {:04}".format(Asteroid.asteroid_score))
        if Asteroid.asteroid_score == self.high_score:
            display_text.append("YOU HAVE A NEW HIGH SCORE!")
        else:
            display_text.append("The high schore is {:04}".format(self.high_score))

        text_area_height = len(display_text) * (pyxel.constants.FONT_HEIGHT + 2) - 2
        pyxel.rect(
            0,
            constants.DEATH_HEIGHT - 2,
            pyxel.width,
            constants.DEATH_HEIGHT + text_area_height,
            constants.DEATH_STRIP_COLOUR,
        )

        for i, text in enumerate(display_text):
            y_offset = (pyxel.constants.FONT_HEIGHT + 2) * i
            text_x = center_text(text, pyxel.width, pyxel.constants.FONT_WIDTH)
            pyxel.text(
                text_x,
                constants.DEATH_HEIGHT + y_offset,
                text,
                constants.DEATH_TEXT_COLOUR,
            )


if __name__ == "__main__":
    Game()
