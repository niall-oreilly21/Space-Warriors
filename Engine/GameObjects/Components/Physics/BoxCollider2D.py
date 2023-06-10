import pygame
from pygame import Rect, draw, Vector2
from Engine.GameObjects.Components.Component import Component
from Engine.Graphics.Materials.TextureMaterial2D import TextureMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D


class BoxCollider2D(Component):
    def __init__(self, name, anchor=pygame.Vector2(0, 0)):
        super().__init__(name)
        self.__animator = None
        self.__width = None
        self.__height = None
        self.__anchor = anchor
        self.__color = (255, 0, 0)
        self.__rend = None
        self.__scale = Vector2(1, 1)
        self.__offset = Vector2(0, 0)

    def start(self):
        self.__rend = self._parent.get_component(Renderer2D)
        self.__animator = self._parent.get_component(SpriteAnimator2D)

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, scale):
        self.__scale = scale

    @property
    def offset(self):
        return self.__offset

    @offset.setter
    def offset(self, offset):
        self.__offset = offset

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
        if self.bounds.right > other_collider.bounds.left > self.bounds.left:
            displacement.x = other_collider.bounds.left - self.bounds.right
        elif self.bounds.left < other_collider.bounds.right < self.bounds.right:
            displacement.x = other_collider.bounds.right - self.bounds.left

        if self.bounds.bottom > other_collider.bounds.top > self.bounds.top:
            displacement.y = other_collider.bounds.top - self.bounds.bottom
        elif self.bounds.top < other_collider.bounds.bottom < self.bounds.bottom:
            displacement.y = other_collider.bounds.bottom - self.bounds.top

        return displacement

    @property
    def bounds(self):
        material_source_rect = None

        if isinstance(self.__rend, SpriteRenderer2D):

            if self.__animator:
                material_source_rect = self.__animator.get_current_sprite().source_rect
            if self.__rend.sprite:
                material_source_rect = self.__rend.sprite.source_rect

        if material_source_rect is None:
            material_source_rect = self.__rend.material.source_rect


        bounds = Rect(self._transform.position.x, self._transform.position.y,
                      material_source_rect.width * self.transform.scale.x,
                      material_source_rect.height * self.transform.scale.y)

        rotated_surface = pygame.transform.rotate(pygame.Surface((bounds.width, bounds.height)),
                                                  -self._transform.rotation)
        rotated_bounds = rotated_surface.get_rect(center=bounds.center)
        rotated_bounds.scale_by_ip(self.__scale.x, self.__scale.y)
        rotated_bounds.move_ip(self.__offset.x, self.__offset.y)

        return rotated_bounds

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

    def draw(self, screen, camera_position):
        if isinstance(self.__rend.material, TextureMaterial2D):
            bounds = self.bounds

            bounds.x -= camera_position.x
            bounds.y -= camera_position.y

            rotated_surface = pygame.transform.rotate(pygame.Surface((bounds.width, bounds.height)),
                                                      -self._transform.rotation)
            rotated_bounds = rotated_surface.get_rect(center=bounds.center)
            self.__width = rotated_bounds.width

            self.__height = rotated_bounds.height

            pygame.draw.rect(screen, self.__color, bounds, 4)

    def clone(self):
        box_collider = BoxCollider2D(self._name, self.__anchor.copy())
        box_collider.scale = self.__scale
        box_collider.offset = self.__offset
        return box_collider
