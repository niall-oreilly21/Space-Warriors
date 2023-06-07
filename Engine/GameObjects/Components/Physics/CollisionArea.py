import math

import pygame


class CollisionArea:
        def __init__(self, x, y, width, height):
            self.__x = x
            self.__y = y
            self.__width = width
            self.__height = height

        @property
        def x(self):
            return self.__x

        @property
        def y(self):
            return self.__y

        @x.setter
        def x(self, x):
            self.__x = x

        @y.setter
        def y(self, y):
            self.__y = y

        @property
        def width(self):
            return self.__width

        @property
        def height(self):
            return self.__height

        @property
        def boundary(self):
            return pygame.Rect(self.__x, self.__y, self.__width, self.__height)






