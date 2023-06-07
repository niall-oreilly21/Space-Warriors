import math

import pygame

from App.Constants.Application import Application


class CollisionRange:
        def __init__(self, x, y, width, height):
            self.__bounds = pygame.Rect(x, y, width, height)

        @property
        def x(self):
            return self.__bounds.x

        @property
        def y(self):
            return self.__bounds.y

        @x.setter
        def x(self, x):
            self.__bounds.x = x

        @y.setter
        def y(self, y):
            self.__bounds.y = y

        @property
        def width(self):
            return self.__bounds.width

        @property
        def height(self):
            return self.__bounds.height

        @property
        def bounds(self):
            return self.__bounds

        def draw(self, screen, camera_position):
            self.x -=  camera_position.x
            self.y -=  camera_position.y
            print(camera_position.x)
            pygame.draw.rect(screen, (255, 255, 255), self.__bounds, 5)






