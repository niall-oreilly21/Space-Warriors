import pygame
from pygame import Rect, draw, Vector2
from Engine.GameObjects.Components.Component import Component
from Engine.Graphics.Materials.TextureMaterial2D import TextureMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D


class BoxCollider2D(Component):
    def __init__(self, name, anchor=pygame.Vector2(0, 0)):
        super().__init__(name)
        self.__anchor = anchor
        self.__color = (255, 0, 0)
        self.__rend = None

    def start(self):
        self.__rend = self._parent.get_component(Renderer2D)

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

    def calculate_displacement_vector(self, other_collider):
        displacement = pygame.Vector2(0, 0)

        # Calculate the minimum translation distance to separate the colliders
        if self.bounds.right > other_collider.bounds.left and self.bounds.left < other_collider.bounds.left:
            displacement.x = other_collider.bounds.left - self.bounds.right
        elif self.bounds.left < other_collider.bounds.right and self.bounds.right > other_collider.bounds.right:
            displacement.x = other_collider.bounds.right - self.bounds.left

        if self.bounds.bottom > other_collider.bounds.top and self.bounds.top < other_collider.bounds.top:
            displacement.y = other_collider.bounds.top - self.bounds.bottom
        elif self.bounds.top < other_collider.bounds.bottom and self.bounds.bottom > other_collider.bounds.bottom:
            displacement.y = other_collider.bounds.bottom - self.bounds.top

        return displacement


    @property
    def bounds(self):

        material_source_rect = self.__rend.material.source_rect

        bounds = Rect(self._transform.position.x, self._transform.position.y, material_source_rect.width * self.transform.scale.x,
                      material_source_rect.height * self.transform.scale.y)

        rotated_surface = pygame.transform.rotate(pygame.Surface((bounds.width, bounds.height)),
                                                  -self._transform.rotation)
        rotated_bounds = rotated_surface.get_rect(center=bounds.center)
        self.__bounds = rotated_bounds

        return self.__bounds

    @property
    def size(self):
        return pygame.Vector2(self.bounds.width, self.bounds.height)

    def collides_with(self, other_collider):
        return self.bounds.colliderect(other_collider.bounds)

    def update(self, game_time):
        pass


     # Calculate the distance between two colliders
    def distance_to(self, other_collider):
        self_center = Vector2(self.bounds.centerx, self.bounds.centery)
        other_center = Vector2(other_collider.bounds.centerx, other_collider.bounds.centery)
        return self_center.distance_to(other_center)

    def draw(self, screen, camera_manager):
        if isinstance(self.__rend.material, TextureMaterial2D):
            bounds = self.bounds

            bounds.x -= camera_manager.active_camera.transform.position.x
            bounds.y -= camera_manager.active_camera.transform.position.y

            rotated_surface = pygame.transform.rotate(pygame.Surface((bounds.width, bounds.height)),
                                                      -self._transform.rotation)
            rotated_bounds = rotated_surface.get_rect(center=bounds.center)
            self.__width = rotated_bounds.width
            #print(self.__width)
            self.__height = rotated_bounds.height

            pygame.draw.rect(screen, self.__color, bounds, 4)

    def clone(self):
        return BoxCollider2D(self._name, self.__anchor.copy())