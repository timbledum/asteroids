"""Module for keeping track of and detecting collisions."""

from itertools import product
import sound


def detect_collision(object1, object2):
    """Detects whether a collision has been made between two objects.
    
    Assumes both objects are circles and have x, y and radius attributes."""

    x_dist = object1.x - object2.x
    y_dist = object1.y - object2.y

    total_radius = object1.radius + object2.radius
    return (x_dist * x_dist + y_dist * y_dist) < (total_radius * total_radius)


def detect_ship_asteroid_collisions(ship, asteroid_class):
    """Iterate between the asteroids to detect collisions between the ship and asteroids."""
    test_cases = ((ship, asteroid) for asteroid in asteroid_class.asteroids)
    return any((detect_collision(*test_case) for test_case in test_cases))


def return_first_match(element, lst, test):
    """Helper function to find the first match in a list based on a custom test."""
    for i in lst:
        if test(element, i):
            return i


def detect_bullet_asteroid_collisions(bullet_class, asteroid_class):
    """Detect collisions between bullets and asteroids.

    For each asteroid, search through bullets for a collision. If there
    is, delete both the asteroid and the bullet."""

    asteroid_destroy_list = []
    for asteroid in asteroid_class.asteroids.copy():
        bullet = return_first_match(asteroid, bullet_class.bullets, detect_collision)
        if bullet:
            bullet.destroy()
            asteroid.destroy()
            sound.hit()
