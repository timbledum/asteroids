"""The ship module.

Defines the ship class, and the ship-breakup class (for when
death happens)."""

import math
import random

import pyxel

from bullet import Bullet
from utils import check_bounds, rotate_around_origin, Point

import constants
import sound


class Ship:
    """The ship class.

    The ship class describes the behaviour and rendering of the ships. This includes:
    - initial creation
    - resetting on new game
    - control (rotation, acceleration and shooting)
    """

    radius = constants.SHIP_RADIUS

    def __init__(self, x, y, colour):
        """Set up initial variables."""
        self.starting_x = x
        self.starting_y = y
        self.starting_colour = colour
        self.reset()
        self.accelerating = False
        self.shooting = False

    def reset(self):
        """Reset the game specific variables (position, momentum and direction)."""
        self.x = self.starting_x
        self.y = self.starting_y
        self.colour = self.starting_colour
        self.direction = 0
        self.momentum_x = 0
        self.momentum_y = 0

        self.points = []
        for point in constants.SHIP_POINTS:
            self.points.append(Point(*point))

    def rotate(self, direction):
        """Rotate the ship based on user input."""
        if direction == "l":
            multipler = 1
        elif direction == "r":
            multipler = -1
        else:
            raise ValueError("Direction must be the 'l'eft or 'r'ight")

        rotation_angle = constants.ROTATION * multipler

        for point in self.points:
            point.rotate_point(rotation_angle)

        self.direction += rotation_angle

    def accelerate(self):
        """Increase the velocity (to a maximum) of the ship based on user input."""

        self.accelerating = True

        acc_x, acc_y = rotate_around_origin(
            (0, -constants.ACCELERATION), self.direction
        )
        self.momentum_x += acc_x
        self.momentum_y += acc_y

        acceleration = math.hypot(self.momentum_x, self.momentum_y)
        if acceleration > constants.MAX_ACCELERATION:
            scale = constants.MAX_ACCELERATION / acceleration
            self.momentum_x *= scale
            self.momentum_y *= scale
            assert (
                round(math.hypot(self.momentum_x, self.momentum_y), 0)
                == constants.MAX_ACCELERATION
            )

    def shoot(self):
        """Create a bullet based on the ship's direction and position."""
        vel_x, vel_y = rotate_around_origin(
            (0, -constants.BULLET_VELOCITY), self.direction
        )
        ship_tip = self.points[0]
        Bullet(
            self.points[0].x + self.x,
            self.points[0].y + self.y,
            vel_x,
            vel_y,
            constants.BULLET_COLOUR,
        )

    def yes_shoot(self):
        """Start the shoot sound."""
        if not self.shooting:
            sound.start_shoot()
            self.shooting = True

    def no_shoot(self):
        """End the shoot sound."""
        if self.shooting:
            sound.stop_shoot()
            self.shooting = False

    def destroy(self):
        """Destroy the ship (does nothing at this point)."""
        pass

    def update_position(self):
        """Update the position and reduce the velocity."""
        self.x += self.momentum_x
        self.y += self.momentum_y
        self.momentum_x *= constants.DRAG
        self.momentum_y *= constants.DRAG

        self.x = check_bounds(self.x, pyxel.width, constants.BUFFER)
        self.y = check_bounds(self.y, pyxel.height, constants.BUFFER)

    def display(self):
        """Display lines between each point and display the exhaust if accelerating."""

        for point1, point2 in zip(self.points, self.points[1:] + [self.points[0]]):
            pyxel.line(
                x1=point1.x + self.x,
                y1=point1.y + self.y,
                x2=point2.x + self.x,
                y2=point2.y + self.y,
                col=self.colour,
            )

        if self.accelerating:
            self.display_acceleration()

    def display_acceleration(self):
        """Display the exhaust if accelerating."""
        x1, y1 = rotate_around_origin(
            (0, constants.SHIP_ACCELERATION_POINTS[0]), self.direction
        )
        x2, y2 = rotate_around_origin(
            (0, constants.SHIP_ACCELERATION_POINTS[1]), self.direction
        )
        pyxel.line(
            x1=x1 + self.x,
            y1=y1 + self.y,
            x2=x2 + self.x,
            y2=y2 + self.y,
            col=constants.SHIP_ACCELERATION_COLOUR,
        )


class ShipBreakup:
    """A class based on the ship on death which displays the various segements
    drifting aimlessly in space."""

    def __init__(self, ship):
        """Coppies key parameters from ship and constructs the lines to drift."""
        self.segments = []

        def random_velocity():
            """Helper function to determine a random velocity."""
            direction = random.random() * math.pi * 2
            velocity = rotate_around_origin(
                (0, -constants.SHIP_DRIFT_VELOCITY), direction
            )
            return velocity

        for point1, point2 in zip(ship.points, ship.points[1:] + [ship.points[0]]):
            rvel_x, rvel_y = random_velocity()
            line_velocity = (rvel_x + ship.momentum_x, rvel_y + ship.momentum_y)
            spin = constants.SHIP_BREAKUP_ROTATION * random.choice((-1, 1))

            line = Line.line_from_two_points(
                point1.x + ship.x,
                point1.y + ship.y,
                point2.x + ship.x,
                point2.y + ship.y,
                velocity=line_velocity,
                spin=spin,
                colour=ship.colour,
            )
            self.segments.append(line)

    def update(self):
        """Drift the ship segments."""
        for segment in self.segments:
            segment.update()

    def display(self):
        """Display lines between each point."""
        for segment in self.segments:
            segment.display()


class Line:
    """Class to contain a rotating line segment."""

    def __init__(self, x, y, length, direction, velocity, spin, colour):
        """Initialise variables and set ends of the line.
        
        The provided x and y are of the center point."""
        self.x = x
        self.y = y
        self.length = length
        self.direction = direction
        self.vel_x, self.vel_y = velocity
        self.spin = spin
        self.colour = colour

        self.points = []
        for end in (1, -1):
            self.points.append(Point(0, end * self.length / 2))

        self.rotate(direction)

    @classmethod
    def line_from_two_points(cls, x1, y1, x2, y2, velocity, spin, colour):
        """Construct a line from two points rather than a point, a direction, and a length."""
        x = sum((x1, x2)) / 2
        y = sum((y1, y2)) / 2
        length = math.hypot(x1 - x2, y1 - y2)
        direction = -math.atan2(y1 - y2, x1 - x2) - math.pi / 2
        return cls(x, y, length, direction, velocity, spin, colour)

    def rotate(self, radians):
        """Rotate both points around center."""
        for point in self.points:
            point.rotate_point(radians)

    def update(self):
        """Update the position and rotate."""
        self.x += self.vel_x
        self.y += self.vel_y

        self.vel_x *= constants.SHIP_BREAKUP_DRAG
        self.vel_y *= constants.SHIP_BREAKUP_DRAG

        self.x = check_bounds(self.x, pyxel.width, constants.BUFFER)
        self.y = check_bounds(self.y, pyxel.height, constants.BUFFER)

        self.rotate(self.spin)

    def display(self):
        """Display lines between each point and display the exhaust if accelerating."""
        point1, point2 = self.points
        pyxel.line(
            x1=point1.x + self.x,
            y1=point1.y + self.y,
            x2=point2.x + self.x,
            y2=point2.y + self.y,
            col=self.colour,
        )
