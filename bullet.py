"""The bullet class."""


import pyxel
import constants


class Bullet:
    """The bullet class.

    The bullet class describes the behaviour and rendering of the bullets. This includes:
    - initial creation
    - movement

    On the class level, it also keeps track of all bullets in play (and can
    render all at once)."""

    bullets = []
    radius = constants.BULLET_RADIUS

    def __init__(self, x, y, velocity_x, velocity_y, colour):
        """Set the bullet key variables and and the bullet to the collection of bullets."""
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.colour = colour

        Bullet.bullets.append(self)

    def update(self):
        """Update the position based on the velocity, and destroy if out of bounds."""
        self.x += self.velocity_x
        self.y += self.velocity_y

        if (
            (self.x < 0)
            or (self.y < 0)
            or (self.x > pyxel.width)
            or (self.y > pyxel.width)
        ):
            self.destroy()

    def destroy(self):
        """Remove the current bullet from the collection."""
        Bullet.bullets.remove(self)
        del self

    def display(self):
        """Display the bullet as a line."""
        pyxel.line(
            x1=self.x,
            y1=self.y,
            x2=self.x + self.velocity_x,
            y2=self.y + self.velocity_y,
            col=self.colour,
        )

    @staticmethod
    def update_all():
        """Convenience function to update all bullets."""
        for bullet in Bullet.bullets:
            bullet.update()

    @staticmethod
    def display_all():
        """Convenience function to display all bullets."""
        for bullet in Bullet.bullets:
            bullet.display()
