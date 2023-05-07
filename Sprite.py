import pygame

class Sprite:
    def __init__(self, texture, source_rect, color=(255, 255, 255), alpha=255, pivot=(0.5, 0.5)):
        self.texture = texture
        self.source_rect = source_rect
        self.color = color
        self.alpha = alpha
        self.pivot = pivot

