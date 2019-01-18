"""Module for keeping track and detecting collisions."""

from itertools import product

def detect_collision(object1, object2):
    """Detects whether a collision has been made between two objects.
    
    Assumes both objects are circles and have x, y and radius attributes."""

    x_dist = object1.x - object2.x 
    y_dist = object1.y - object2.y

    total_radius = object1.radius + object2.radius
    return (x_dist * x_dist + y_dist * y_dist) < (total_radius * total_radius)

def detect_ship_asteroid_colissions(ship, asteroid_class):
    test_cases = ((ship, asteroid) for asteroid in asteroid_class.asteroids)
    return any((detect_collision(*test_case) for test_case in test_cases))


def return_first_match(element, lst, test):
    for i in lst:
        if test(element, i):
            return i

def detect_bullet_asetoid_colissions(bullet_class, asteroid_class):
    asteroid_destroy_list = []
    for asteroid in asteroid_class.asteroids.copy():
        bullet = return_first_match(asteroid, bullet_class.bullets, detect_collision)
        if bullet:
            bullet.destroy()
            asteroid.destroy()