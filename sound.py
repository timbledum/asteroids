"""Module with convenience functions for triggering various sound events."""

from pathlib import Path

import pyxel

import constants


def init_music():
    file = Path(__file__).parent / constants.SOUND_FILE
    pyxel.load(str(file))


def start_shoot():
    pyxel.play(0, 0, loop=True)


def stop_shoot():
    pyxel.stop(0)


def start_accelerate():
    pyxel.play(1, 2, loop=True)


def stop_accelerate():
    pyxel.stop(1)


def spawn():
    pyxel.play(2, 1)


def hit():
    pyxel.play(2, 4)


def death():
    pyxel.stop()
    pyxel.play(2, 3)
