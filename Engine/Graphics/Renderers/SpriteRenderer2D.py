import pygame
from pygame import Rect

from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D

class SpriteRenderer2D(Renderer2D):
    def __init__(self, name, material, layer, sprite=None):
        super().__init__(name, material, layer)
        self.__sprite = sprite
        self.__flip_x = False
        self.__flip_y = False
        self.__animator = None

    def start(self):
        self.__animator = self.parent.get_component(SpriteAnimator2D)

    @property
    def flip_x(self):
        return self.__flip_x

    @property
    def sprite(self):
        return self.__sprite

    @property
    def flip_y(self):
        return self.__flip_y

    @flip_x.setter
    def flip_x(self, flip_x):
        self.__flip_x = flip_x

    @flip_y.setter
    def flip_y(self, flip_y):
        self.__flip_y = flip_y

    def draw(self, surface, transform):

        if self.__animator is not None:
            self.__sprite = self.__animator.get_current_sprite()

        if self.__sprite:
            self._material.texture = self.__sprite.texture
            self._material.source_rect = self.__sprite.source_rect
            self._material.color = self.__sprite.color
            self._material.alpha = self.__sprite.alpha
            self._material.origin = self.__sprite.pivot
            self._material.flip_x = self.__flip_x
            self._material.flip_y = self.__flip_y
            super().draw(surface, transform)

    def clone(self):
        return SpriteRenderer2D(self._name, self._material.clone(), self._layer)



