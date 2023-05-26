import pygame
from pygame import Rect, draw, Vector2
from Engine.GameObjects.Components.Component import Component
from Engine.Graphics.Materials.TextureMaterial2D import TextureMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D


class BoxCollider2D(Component):
    def __init__(self, name, width, height, anchor=(0, 0)):
        super().__init__(name)
        self.__width = width
        self.__height = height
        self.__anchor = anchor
        self.__color = (255, 0, 0)  # Color of the collider

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        self.__width = value

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        self.__height = value

    @property
    def anchor(self):
        return self.__anchor

    @anchor.setter
    def anchor(self, value):
        self.__anchor = value

    @property
    def bounds(self):
        material_source_rect = self._parent.get_component(Renderer2D).material.source_rect
        return Rect(self._transform.position.x,  self._transform.position.y, material_source_rect.width * self.transform.scale.x, material_source_rect.height * self.transform.scale.y)

    def collides_with(self, other_collider):
        return self.bounds.colliderect(other_collider.bounds)

    def update(self, game_time):
        pass

    def draw(self, screen, cameraManager):
        bounds = self.bounds

        bounds.x -= cameraManager.active_camera.transform.position.x
        bounds.y -= cameraManager.active_camera.transform.position.y
        pygame.draw.rect(screen, self.__color, bounds, 1)
