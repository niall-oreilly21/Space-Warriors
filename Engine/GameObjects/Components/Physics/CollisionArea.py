import math

import pygame


class CollisionArea:
        def __init__(self, x, y, width, height):
            self.__x = x
            self.__y = y
            self.__width = width
            self.__height = height
            self.__left = None
            self.__right = None
            self.__top = None
            self.__bottom = None

        @property
        def left(self):
            return self.__x

        @property
        def right(self):
            return self.__x + self.__width

        @property
        def boundary(self):
            return pygame.Rect(self.__x, self.__y, self.__width, self.__height)

        @property
        def top(self):
            return self.__y

        @property
        def bottom(self):
            return self.__y + self.__height

        @property
        def width(self):
            return self.__width

        @property
        def height(self):
            return self.__height

        def set_x(self, x):
            self.__x = x

        def set_y(self, y):
            self.__y = y

        def intersects_screen(self, range_rect):
            return (
                    self.__x + self.__width > range_rect.x - range_rect.width
                    and self.__x < range_rect.x + range_rect.width
                    and self.__y + self.__height > range_rect.y - range_rect.height
                    and self.__y < range_rect.y + range_rect.height
            )

        def is_in_range(self, rect_one, rect_two, range_distance):
            center1 = rect_one.center
            center2 = rect_two.center
            distance = math.hypot(center2[0] - center1[0], center2[1] - center1[1])
            return distance <= range_distance
