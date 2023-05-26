from Engine.Graphics.Materials.Material2D import Material2D


import pygame

class TextureMaterial2D(Material2D):
    def __init__(self, texture, color, layer_depth, origin, sprite_effects, source_rect=None):
        super().__init__(color, layer_depth, origin, sprite_effects)
        self.texture = texture
        self.source_rect = source_rect or pygame.Rect((0, 0, texture.get_width(), texture.get_height()))

    def draw(self, surface, transform):
        texture_surface = pygame.Surface(self.source_rect.size, pygame.SRCALPHA)
        texture_surface.blit(self.texture, (0, 0), self.source_rect)
        if self._color:
            texture_surface.fill(self._color, special_flags=pygame.BLEND_RGBA_MULT)

        if self._flip_x or self._flip_y:
            texture_surface = pygame.transform.flip(texture_surface, self._flip_x, self._flip_y)

        scaled_surface = pygame.transform.scale(texture_surface, (int(texture_surface.get_width() * transform.scale.x),
                                                                  int(texture_surface.get_height() * transform.scale.y)))

        surface.blit(scaled_surface,(transform.position.x, transform.position.y))







