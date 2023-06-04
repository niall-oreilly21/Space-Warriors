import pygame.math as pgmath
from pygame import Vector3, Vector2

from Engine.Other.Interfaces.ICloneable import ICloneable


class Direction:
    RIGHT = Vector2(1, 0)
    LEFT = Vector2(-1, 0)
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)


class Transform2D(ICloneable):
    def __init__(self, position, rotation, scale):
        self.__position = position
        self.__rotation = rotation
        self.__scale = scale

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        self.__position = position

    @property
    def rotation(self):
        return self.__rotation

    @property
    def scale(self):
        return self.__scale

    def translate_by(self, translate_by):
        self.__position += translate_by

    def translate(self, x, y):
        self.__position += Vector2(x, y)

    @rotation.setter
    def rotation(self, angle):
        self.__rotation += angle

    @scale.setter
    def scale(self, scale):
        self.__scale = scale

    def clone(self):
        return Transform2D(self.__position.copy(), self.__rotation, self.__scale.copy())
