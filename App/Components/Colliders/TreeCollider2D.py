import pygame
from pygame import Rect

from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D


class TreeCollider(BoxCollider2D):
    def __init__(self, name):
        super().__init__(name)

    @property
    def bounds(self):

        self.__rend = self._parent.get_component(Renderer2D)

        material_source_rect = self.__rend.material.source_rect

        if self._parent.name == "Tree":
            width = material_source_rect.width * self.transform.scale.x * 0.3
            height = material_source_rect.height * self.transform.scale.y * 0.15
            position_x = self.transform.position.x + width + 6
            position_y = self.transform.position.y + material_source_rect.height * self.transform.scale.y - height
        else:
            width = material_source_rect.width * self.transform.scale.x * 0.5
            height = material_source_rect.height * self.transform.scale.y * 0.25
            position_x = self.transform.position.x + material_source_rect.width * self.transform.scale.x * 0.25
            position_y = self.transform.position.y + material_source_rect.height * self.transform.scale.y - height

        bounds = Rect(position_x, position_y, width, height)

        rotated_surface = pygame.transform.rotate(pygame.Surface((bounds.width, bounds.height)),
                                                  -self._transform.rotation)
        rotated_bounds = rotated_surface.get_rect(center=bounds.center)

        self.__bounds = rotated_bounds

        return self.__bounds

    def draw(self, screen, camera_position):
        bounds = self.bounds

        bounds.x -= camera_position.x
        bounds.y -= camera_position.y

        rotated_surface = pygame.transform.rotate(pygame.Surface((bounds.width, bounds.height)),
                                                  -self._transform.rotation)
        rotated_bounds = rotated_surface.get_rect(center=bounds.center)
        self.__width = rotated_bounds.width
        # print(self.__width)
        self.__height = rotated_bounds.height

        pygame.draw.rect(screen, (255, 0, 0), bounds, 4)

    def clone(self):
        return TreeCollider(self._name, self.anchor.copy())
