from abc import abstractmethod

import pygame
from pygame import Rect

from Engine.GameObjects.Components.Component import Component
from Engine.Graphics.Materials.RectMaterial2D import RectMaterial2D
from Engine.Graphics.Materials.TextMaterial2D import TextMaterial2D


class Renderer2D(Component):
        def __init__(self, name, material, layer=0, is_drawing = True):
            super().__init__(name)
            self._material = material
            self._layer = layer
            self.__bounds = None
            self.__is_drawing = is_drawing

        @property
        def material(self):
            return self._material

        @material.setter
        def material(self, material):
            self._material = material

        @property
        def layer(self):
            return self._layer

        @layer.setter
        def layer(self, layer):
            self._layer = layer

        @property
        def is_drawing(self):
            return  self.__is_drawing

        @is_drawing.setter
        def is_drawing(self, is_drawing):
             self.__is_drawing = is_drawing

        def draw(self, surface, transform):
            if self.__is_drawing:
                self._material.draw(surface, transform)

        @property
        def bounds(self):
            return Rect(self._transform.position.x, self._transform.position.y,
                          self.__bounds.width * self.transform.scale.x,
                          self.__bounds.height * self.transform.scale.y)

        @bounds.setter
        def bounds(self, bounds):
            self.__bounds = bounds


        def get_bounding_rect(self, transform):
            sprite_rect = self._material.source_rect
            scaled_sprite_rect = pygame.Rect(0, 0, sprite_rect.width * transform.scale.x,
                                             sprite_rect.height * transform.scale.y)
            screen_rect = scaled_sprite_rect.move(transform.position.x - scaled_sprite_rect.width / 2,
                                                  transform.position.y - scaled_sprite_rect.height / 2)
            return screen_rect

        def clone(self):
            return Renderer2D(self._name, self._material.clone(), self._layer, self.__is_drawing)