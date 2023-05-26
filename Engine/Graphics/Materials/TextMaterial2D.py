import math

import pygame
from pygame.math import Vector2
from Engine.Graphics.Materials.Material2D import Material2D

class TextMaterial2D(Material2D):
    def __init__(self, sprite_font, font_name, text, text_offset, color, layer_depth=0, origin=Vector2(0, 0), sprite_effects=None):
        super().__init__(color, layer_depth, origin, sprite_effects)
        self.__sprite_font = sprite_font
        self.__text = text
        self.__text_offset = text_offset
        self.__font_name = font_name

    def _transform_material(self, surface, transform):
        rotated_text_surface = self._rotate_surface(surface, transform.rotation)

        text_position = tuple(transform.position + Vector2(*self.__text_offset) - Vector2(rotated_text_surface.get_size()) / 2)

        return rotated_text_surface, text_position


    def draw(self, surface, transform):
        scaled_font_size = int(self.__sprite_font.size(self.__text)[1] * transform.scale.y)
        scaled_font = pygame.font.Font(self.__font_name, scaled_font_size)

        text_surface = scaled_font.render(self.__text, True, self._color)

        self._blits(surface, text_surface, transform)





