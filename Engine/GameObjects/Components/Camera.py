import numpy as np
import pygame
from pygame import Vector2

from Engine.GameObjects.Components.Component import Component


class Camera(Component):
    def __init__(self, name, viewport_width, viewport_height):
        super().__init__(name)
        self.__viewport = Vector2(viewport_width, viewport_height)

    @property
    def viewport(self):
        return self.__viewport

