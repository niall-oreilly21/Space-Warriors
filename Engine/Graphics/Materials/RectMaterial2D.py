from pygame import Vector2, Surface

import pygame

from Engine.Graphics.Materials.Material2D import Material2D


class RectMaterial2D(Material2D):
    def __init__(self, width, height, color, alpha, origin = Vector2(0,0)):
        super().__init__(color, alpha, origin)
        self.__width = width
        self.__height = height

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        self.__width = width

    def _transform_material(self, surface, transform):
        transformed_surface = pygame.transform.scale(surface, (int(surface.get_width() * transform.scale.x),
                                                                int(surface.get_height() * transform.scale.y)))


        rotated_surface = self._rotate_surface(transformed_surface, transform.rotation)

        shape_position = tuple(transform.position - Vector2(rotated_surface.get_size()) / 2)

        return rotated_surface, shape_position

    def draw(self, surface, transform):
        rect_surface = Surface((self.__width, self.__height))
        rect_surface.fill(self._color)
        self._blits(surface, rect_surface, transform)

    def clone(self):
        return RectMaterial2D(self.__width, self.__height, self._color, self._alpha, self._origin)
