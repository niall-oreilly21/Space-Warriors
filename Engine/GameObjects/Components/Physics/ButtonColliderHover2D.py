import pygame
from pygame import Vector2
from Engine.GameObjects.Components.Physics.ButtonCollider2D import ButtonCollider2D
from Engine.Graphics.Materials.TextMaterial2D import TextMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D


class ButtonColliderHover2D(ButtonCollider2D):
    def __init__(self, name, scale_factor, anchor=pygame.Vector2(0, 0)):
        super().__init__(name, anchor)
        self.__new_text_offset = None
        self.__text_original_offset = None
        self.__text_material = None
        self.__old_scale = None
        self.__x_original_position = None
        self.__y_original_position = None
        self.__new_scale = None
        self.__scale_factor = scale_factor

    def start(self):
        super().start()
        self.__x_original_position = self.transform.position.x
        self.__y_original_position = self.transform.position.y

        self.__old_scale = self.transform.scale.copy()
        self.__new_scale = self.transform.scale + Vector2(self.__scale_factor, self.__scale_factor)

        for renderer in self._parent.get_components(Renderer2D):
            if isinstance(renderer.material, TextMaterial2D):
                self.__text_material = renderer.material
                self.__text_original_offset = self.__text_material.text_offset
                self.__new_text_offset = self.__text_original_offset + Vector2(5, 2.5)

    def mouse_hover(self):
        if self.bounds.collidepoint(self._mouse_position):
            old_bounds = self.bounds
            self.transform.scale = self.__new_scale
            new_bounds = self.bounds
            translation_offset = Vector2(*old_bounds.center) - Vector2(*new_bounds.center)
            self.transform.translate_by(translation_offset)

            if self.__text_material:
                self.__text_material.text_offset = self.__new_text_offset
        else:
            self.transform.scale = self.__old_scale
            self.transform.position = Vector2(self.__x_original_position, self.__y_original_position)

            if self.__text_material:
                self.__text_material.text_offset = self.__text_original_offset

    def update(self, game_time):
        super().update(game_time)
        self.mouse_hover()

    def draw(self, screen, camera_position):
        super().draw(screen, camera_position)

    def clone(self):
        return ButtonColliderHover2D(self._name, self.__scale_factor)
