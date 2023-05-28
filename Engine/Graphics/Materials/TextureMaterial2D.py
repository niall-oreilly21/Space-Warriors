import math

from Engine.Graphics.Materials.Material2D import Material2D


import pygame

class TextureMaterial2D(Material2D):
    def __init__(self, texture, color, origin, alpha=None, source_rect=None):
        if alpha is None:
            alpha = 255
        super().__init__(color, alpha, origin)
        self.__texture = texture
        self.__source_rect = source_rect or pygame.Rect((0, 0, texture.get_width(), texture.get_height()))

    @property
    def texture(self):
        return self.__texture

    @texture.setter
    def texture(self, texture):
        self.__texture = texture

    @property
    def source_rect(self):
        return self.__source_rect

    @source_rect.setter
    def source_rect(self, source_rect):
        self.__source_rect = source_rect

    def _transform_material(self, surface, transform):
        rotated_surface = self._rotate_surface(surface, transform.rotation)

        # Scale the rotated surface
        scaled_surface = pygame.transform.scale(rotated_surface,
                                                (int(rotated_surface.get_width() * transform.scale.x),
                                                 int(rotated_surface.get_height() * transform.scale.y)))

        position = (int(transform.position.x - scaled_surface.get_width() / 2 + self.source_rect.width / 2 * transform.scale.x),
                    int(transform.position.y - scaled_surface.get_height() / 2 + self.source_rect.height / 2 * transform.scale.y))

        return scaled_surface, position

    def draw(self, surface, transform):
        texture_surface = pygame.Surface(self.source_rect.size, pygame.SRCALPHA)
        texture_surface.blit(self.__texture, (0, 0), self.source_rect)
        if self._color:
            texture_surface.fill(self._color, special_flags=pygame.BLEND_RGBA_MULT)

        if self._flip_x or self._flip_y:
            texture_surface = pygame.transform.flip(texture_surface, self._flip_x, self._flip_y)

        self._blits(surface, texture_surface, transform)

    def clone(self):
        return TextureMaterial2D(self.__texture, self._color, self._origin, self._alpha, self.source_rect.copy())





