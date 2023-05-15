from pygame.math import Vector2
from Engine.Graphics.Materials.Material2D import Material2D

class TextMaterial2D(Material2D):
    def __init__(self, sprite_font, text, text_offset, color, layer_depth=0, origin=(0, 0), sprite_effects=None):
        super().__init__(color, layer_depth, origin, sprite_effects)
        self.__sprite_font = sprite_font
        self.__text = text
        self.__text_offset = text_offset

    def draw(self, surface, transform):
        text_position = tuple(transform.position + Vector2(*self.__text_offset))
        surface.blit(self.__sprite_font.render(self.__text, True, self._color), text_position)

