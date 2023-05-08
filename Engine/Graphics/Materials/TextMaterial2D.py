from pygame.math import Vector2
from Engine.Graphics.Materials.Material2D import Material2D

class TextMaterial2D(Material2D):
    def __init__(self, sprite_font, text, text_offset, color, layer_depth=0, origin=(0, 0), sprite_effects=None):
        super().__init__(color, layer_depth, origin, sprite_effects)
        self.sprite_font = sprite_font
        self.text = text
        self.text_offset = text_offset

    def draw(self, surface, transform):
        text_position = tuple(transform.position + Vector2(*self.text_offset))
        surface.blit(self.sprite_font.render(self.text, True, self.color), text_position)

