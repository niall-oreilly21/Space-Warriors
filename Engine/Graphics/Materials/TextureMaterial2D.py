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
        if self.color:
            texture_surface.fill(self.color, special_flags=pygame.BLEND_RGBA_MULT)

        if self.flip_x or self.flip_y:
            texture_surface = pygame.transform.flip(texture_surface, self.flip_x, self.flip_y)

        surface.blit(texture_surface, transform.position)







