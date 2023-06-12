import math

import pygame
from pygame.math import Vector2
from Engine.Graphics.Materials.Material2D import Material2D

class TextMaterial2D(Material2D):
    def __init__(self, sprite_font_file_path, font_size, text, text_offset, color, alpha=255, origin=Vector2(0, 0)):
        super().__init__(color, alpha, origin)
        self.__sprite_font = pygame.font.Font(sprite_font_file_path, font_size)
        self.__text = text
        self.__text_offset = text_offset
        self.__font_name = sprite_font_file_path
        self.__font_size = font_size

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text

    @property
    def text_offset(self):
        return self.__text_offset

    @text_offset.setter
    def text_offset(self, text_offset):
        self.__text_offset = text_offset

    def _transform_material(self, surface, transform):
        rotated_text_surface = self._rotate_surface(surface, transform.rotation)

        text_position = tuple(
            transform.position + Vector2(*self.__text_offset) - Vector2(rotated_text_surface.get_size()) / 2)

        return rotated_text_surface, text_position

    def draw(self, surface, transform):
        scaled_font_size = int(self.__sprite_font.size(self.__text)[1] * transform.scale.y)
        scaled_font = pygame.font.Font(self.__font_name, scaled_font_size)

        text_surface = scaled_font.render(self.__text, True, self._color)

        self._blits(surface, text_surface, transform)

    def clone(self):
        return TextMaterial2D(self.__font_name, self.__font_size, self.__text, self.__text_offset, self._color,
                              self._alpha, self._origin.copy())
