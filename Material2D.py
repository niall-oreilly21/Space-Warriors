from abc import ABC, abstractmethod

import pygame

class Material2D(ABC):
    def __init__(self, color, layer_depth, origin, sprite_effects):
        self.color = color
        self.layer_depth = layer_depth
        self.origin = origin
        self.sprite_effects = sprite_effects

    @abstractmethod
    def draw(self, surface):
        pass


