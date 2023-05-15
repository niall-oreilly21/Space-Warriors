import pygame.math as pgmath
from pygame import Vector3, Vector2


class Direction:
    RIGHT = Vector2(1, 0)
    LEFT = Vector2(-1, 0)
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)

import math
import pygame.math
class Transform2D:
    def __init__(self, position, rotation, scale):
        self.position = position
        self.rotation = rotation
        self.scale = scale

    def translate_by(self, translate_by):
        self.position += translate_by

    def translate(self, x, y):
        self.position += Vector2(x, y)

    def rotate(self, angle):
        self.rotation += angle

    def scale_by(self, x, y, z):
        self.scale *= Vector2(x, y)

