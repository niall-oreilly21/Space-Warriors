from abc import abstractmethod

import pygame

from Engine.GameObjects.Components.Component import Component


class Renderer2D(Component):
        def __init__(self, name, material, layer=0):
            super().__init__(name)
            self._material = material
            self._layer = layer

        @property
        def material(self):
            return self._material

        @material.setter
        def material(self, material):
            self._material = material

        @property
        def layer(self):
            return self._layer

        def draw(self, surface, transform):
            self._material.draw(surface, transform)

        def get_bounding_rect(self, transform):
            sprite_rect = self._material.source_rect
            scaled_sprite_rect = pygame.Rect(0, 0, sprite_rect.width * transform.scale.x,
                                             sprite_rect.height * transform.scale.y)
            screen_rect = scaled_sprite_rect.move(transform.position.x - scaled_sprite_rect.width / 2,
                                                  transform.position.y - scaled_sprite_rect.height / 2)
            return screen_rect

        def clone(self):
            return Renderer2D(self._name, self._material.clone(), self._layer)