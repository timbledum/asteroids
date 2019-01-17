"""Module to contain constants."""

# General constants #
BUFFER = 7
BACKGROUND_COLOUR = 13

# Ship related constants #
SHIP_COLOUR = 14
SHIP_INITIAL_POSITION = (100, 100)
SHIP_POINTS = [(0, -8), (4, 4), (0, 2), (-4, 4)]
ROTATION = 0.1
DRAG = 0.98
ACCELERATION = 0.4
MAX_ACCELERATION = 6
SHIP_RADIUS = 4

# Bullet related constants #
BULLET_COLOUR = 11
BULLET_VELOCITY = 5
BULLET_RADIUS = 1

# Asteriod related constants #
ASTEROID_COLOUR = 6
ASTEROID_INITIAL_QUANTITY = 3
ASTEROID_ROTATION = 0.02
ASTEROID_SHAPES = [
    [
        (0, 15),
        (4, 9),
        (11, 5),
        (15, 1),
        (5, -3),
        (0, -14),
        (-6, -4),
        (-17, -4),
        (-12, 9),
    ],
    [
        (1, 16),
        (6, 12),
        (6, 6),
        (17, 2),
        (9, -12),
        (1, -17),
        (-4, -2),
        (-18, -4),
        (-11, 8),
    ],
    [
        (0, 17),
        (7, 10),
        (4, 8),
        (14, -1),
        (5, -2),
        (1, -16),
        (-6, -2),
        (-16, -4),
        (-11, 6),
    ],
]
ASTEROID_RADIUS = 16
ASTERPOD_INITIAL_SIZE = 2
ASTEROID_SPLITS = 3
