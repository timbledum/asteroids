import pyxel
import constants


class Bullet:
    bullets = []
    radius = constants.BULLET_RADIUS

    def __init__(self, x, y, velocity_x, velocity_y, colour):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.colour = colour

        Bullet.bullets.append(self)

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if (
            (self.x < 0)
            or (self.y < 0)
            or (self.x > pyxel.width)
            or (self.y > pyxel.width)
        ):
            Bullet.bullets.remove(self)
            del self

    def display(self):
        pyxel.line(
            x1=self.x,
            y1=self.y,
            x2=self.x + self.velocity_x,
            y2=self.y + self.velocity_y,
            col=self.colour,
        )

    @staticmethod
    def update_all():
        for bullet in Bullet.bullets:
            bullet.update()

    @staticmethod
    def display_all():
        for bullet in Bullet.bullets:
            bullet.display()
