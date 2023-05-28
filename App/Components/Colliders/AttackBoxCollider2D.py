import pygame
from pygame import Rect

from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Other.Enums.GameObjectEnums import GameObjectDirection


class AttackBoxCollider2D(BoxCollider2D):
    def __init__(self, name, box_collider, player_controller):
        super().__init__(name)
        self.__box_collider = box_collider
        self.__player_controller = player_controller

    @property
    def bounds(self):

        self.__rend = self._parent.get_component(Renderer2D)

        previous_direction = self.__player_controller.previous_direction

        material_source_rect = self.__rend.material.source_rect

        bounds = Rect(0, 0, 0, 0)
        if previous_direction == GameObjectDirection.Up:
            bounds = Rect(self._transform.position.x, self._transform.position.y,
                          material_source_rect.width * self.transform.scale.x,
                          material_source_rect.height * self.transform.scale.y * 0.5)
        elif previous_direction == GameObjectDirection.Down:
            bounds = Rect(self._transform.position.x, self._transform.position.y + material_source_rect.height / 2,
                          material_source_rect.width * self.transform.scale.x,
                          material_source_rect.height * self.transform.scale.y * 0.5)
        elif previous_direction == GameObjectDirection.Left:
            bounds = Rect(self._transform.position.x, self._transform.position.y,
                          material_source_rect.width * self.transform.scale.x * 0.5,
                          material_source_rect.height * self.transform.scale.y)
        elif previous_direction == GameObjectDirection.Right:
            bounds = Rect(self._transform.position.x + material_source_rect.width / 2, self._transform.position.y,
                          material_source_rect.width * self.transform.scale.x * 0.5,
                          material_source_rect.height * self.transform.scale.y)

        rotated_surface = pygame.transform.rotate(pygame.Surface((bounds.width, bounds.height)),
                                                  -self._transform.rotation)
        rotated_bounds = rotated_surface.get_rect(center=bounds.center)

        self.__bounds = rotated_bounds

        return self.__bounds

    def draw(self, screen, camera_manager):
        pass
        bounds = self.bounds

        bounds.x -= camera_manager.active_camera.transform.position.x
        bounds.y -= camera_manager.active_camera.transform.position.y

        rotated_surface = pygame.transform.rotate(pygame.Surface((bounds.width, bounds.height)),
                                                  -self._transform.rotation)
        rotated_bounds = rotated_surface.get_rect(center=bounds.center)
        self.__width = rotated_bounds.width
        # print(self.__width)
        self.__height = rotated_bounds.height

        pygame.draw.rect(screen, (0,255,0), bounds, 4)
    #
    def clone(self):
        return AttackBoxCollider2D(self._name, self.anchor.copy())
