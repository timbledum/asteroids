"""# Asteroids #
## The classic game of asteroids implemented in [Pyxel](https://github.com/kitao/pyxel)! ##

Controls are **→** & **←** for turning, **↑** for acceleration and **space** for shooting! 

**Q**: Quit the game

![Screenshot!](https://github.com/timbledum/asteroids/blob/master/asteroids.gif)

## Features: ##

1. Moving!
2. Shooting!
3. Enemies (asteroids)!
4. Sound effects!
5. High scores!
6. More?

## Installation ##

1. Install [Python 3](https://www.python.org)
2. Install [Pyxel](https://github.com/kitao/pyxel) using their instructions
3. Clone or copy this repository
4. `python3 main.py` at the command line (if on windows use `py main.py`).


"""

import pyxel

from asteroid import Asteroid
from bullet import Bullet
import collisions
import constants
from utils import center_text, get_highscore, save_highscore
from ship import Ship, ShipBreakup
import sound


class Game:
    """Manage the game state and various classes."""

    def __init__(self):
        """Initialise pyxel and various classes and variables (one off)."""

        pyxel.init(200, 200, scale=2)
        self.ship = Ship(*constants.SHIP_INITIAL_POSITION, constants.SHIP_COLOUR)
        Asteroid.init_class(self.ship)
        sound.init_music()

        self.reset_game()
        self.high_score = get_highscore(constants.HIGH_SCORE_FILE)

        pyxel.run(self.update, self.draw)

    def reset_game(self):
        """Initialise start of game state (reset ship position, score, and asteroids)."""
        self.ship.reset()
        Asteroid.initiate_game()
        self.death = False
        self.spawn_speed = constants.INITIAL_SPAWN_FREQUENCY
        self.next_spawn = pyxel.frame_count + self.spawn_speed

    def update(self):
        """Update the game state, including the asteroids, ship and bullets."""
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
        """Check for input and modify the game state accordingly."""
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
        """Check for collisions between the ship and asteroids, and the bullet and asteroids."""
        if collisions.detect_ship_asteroid_collisions(self.ship, Asteroid):
            self.death_event()

        collisions.detect_bullet_asteroid_collisions(Bullet, Asteroid)

    def death_event(self):
        """Modify game state for when the ship hits and asteroid."""
        self.ship.destroy()
        self.ship_breakup = ShipBreakup(self.ship)
        self.death = True
        sound.death()

        if Asteroid.asteroid_score > self.high_score:
            self.high_score = Asteroid.asteroid_score
            save_highscore(constants.HIGH_SCORE_FILE, self.high_score)

    def check_spawn_asteroid(self):
        """Keep track of the time and spawn new asteroids when appropriate.
        
        Asteroids spawn on a reducing time scale (time decreases by a certain percentage each time."""
        if pyxel.frame_count >= self.next_spawn:
            Asteroid()
            self.next_spawn += self.spawn_speed
            self.spawn_speed *= constants.SPAWN_FREQUENCY_MOVEMENT
            sound.spawn()

    def draw(self):
        """Master method for drawing the board. Mainly calls the display methods of the various classes."""
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
            self.ship_breakup.display()
            self.draw_death()

    def draw_score(self):
        """Draw the score and the high score at the top."""

        score = "{:04}".format(Asteroid.asteroid_score)
        high_score = "HS:{:04}".format(self.high_score)
        high_score_x = pyxel.width - 2 - (7 * pyxel.constants.FONT_WIDTH)

        pyxel.text(3, 3, score, constants.SCORE_COLOUR)
        pyxel.text(high_score_x, 3, high_score, constants.SCORE_COLOUR)

    def draw_death(self):
        """Draw the display text for the end of the game with the score."""
        display_text = ["YOU DIED"]
        display_text.append("Your score is {:04}".format(Asteroid.asteroid_score))
        if Asteroid.asteroid_score == self.high_score:
            display_text.append("YOU HAVE A NEW HIGH SCORE!")
        else:
            display_text.append("The high score is {:04}".format(self.high_score))
        display_text.append("(Q)uit or (R)estart")

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
