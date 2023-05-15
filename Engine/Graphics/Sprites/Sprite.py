import pygame

class Sprite:
    def __init__(self, texture, source_rect, color=(255, 255, 255), alpha=255, pivot=(0.5, 0.5)):
        self.__texture = texture
        self.__source_rect = source_rect
        self.__color = color
        self.__alpha = alpha
        self.__pivot = pivot

    @property
    def texture(self):
        return self.__texture

    @property
    def source_rect(self):
        return self.__source_rect

    @property
    def color(self):
        return self.__color

    @property
    def alpha(self):
        return self.__alpha

    @property
    def pivot(self):
        return self.__pivot

