import pygame

from enum import Enum

from pygame import Vector2


class Direction:
    RIGHT = Vector2(1, 0)
    LEFT = Vector2(-1, 0)
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)


class Transform2D:
    def __init__(self, position, rotation, scale):
        self.position = position
        self.rotation = rotation
        self.scale = scale

    def translate_by(self, translate_by):
        self.position += translate_by
