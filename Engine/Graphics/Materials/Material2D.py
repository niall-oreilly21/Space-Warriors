from abc import ABC, abstractmethod

import pygame

from Engine.Other.Interfaces.ICloneable import ICloneable


class Material2D(ICloneable, ABC):
    def __init__(self, color, alpha, origin):
        self._color = color
        self._alpha = alpha
        self._origin = origin
        self._flip_x = False
        self._flip_y = False

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, alpha):
        self._alpha = alpha

    @property
    def origin(self):
        return self.__origin

    @origin.setter
    def origin(self, origin):
        self.__origin = origin

    @property
    def flip_x(self):
        return self._flip_x

    @flip_x.setter
    def flip_x(self, flip_x):
        self._flip_x = flip_x

    @property
    def flip_y(self):
        return self._flip_y

    @flip_y.setter
    def flip_y(self, flip_y):
        self._flip_y = flip_y

    def _rotate_surface(self, surface, rotation):
        return pygame.transform.rotate(surface, rotation)

    @abstractmethod
    def _transform_material(self, surface, transform):
        pass

    def _blits(self, surface, material_surface, transform):
        material_surface.set_alpha(self._alpha)
        surface.blit(self._transform_material(material_surface, transform)[0],
                     self._transform_material(material_surface, transform)[1])

    @abstractmethod
    def draw(self, surface, transform):
        pass

    def clone(self):
        pass


