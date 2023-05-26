from abc import ABC, abstractmethod

import pygame

class Material2D(ABC):
    def __init__(self, color, layer_depth, origin, sprite_effects):
        self._color = color
        self.__layer_depth = layer_depth
        self.__origin = origin
        self.__sprite_effects = sprite_effects
        self._flip_x = False
        self._flip_y = False

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def layer_depth(self):
        return self.__layer_depth

    @layer_depth.setter
    def layer_depth(self, layer_depth):
        self.__layer_depth = layer_depth

    @property
    def origin(self):
        return self.__origin

    @origin.setter
    def origin(self, origin):
        self.__origin = origin

    @property
    def sprite_effects(self):
        return self.__sprite_effects

    @sprite_effects.setter
    def sprite_effects(self, sprite_effects):
        self.__sprite_effects = sprite_effects

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

    def _blits(self, surface, texture_surface, transform):
        surface.blit(self._transform_material(texture_surface, transform)[0],
                     self._transform_material(texture_surface, transform)[1])

    @abstractmethod
    def draw(self, surface, transform):
        pass


