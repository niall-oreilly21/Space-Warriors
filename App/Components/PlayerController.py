from pygame import Vector2

from Engine.GameObjects.Components.Component import Component
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Managers.CameraManager import CameraManager
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.InputHandler import InputHandler
from Engine.Other.Interfaces.IMoveable import IMoveable
import pygame

from Engine.Other.Transform2D import Direction


class PlayerController(Component, IMoveable):

    def __init__(self, name, speed_x, speed_y):
        super().__init__(name)
        self.__input_handler = InputHandler()
        self.__speed_x = speed_x
        self.__speed_y = speed_y
        self.__tap_threshold = 200

    def update(self, game_time):
        self._parent.get_component(Rigidbody2D).velocity = Vector2(0, 0)
        self.__input_handler.update()
        self._move_left()
        self._move_right()
        self._move_up()
        self._move_down()

    def _move_left(self):
        if self.__input_handler.is_tap(pygame.K_LEFT, self.__tap_threshold):
                self._parent.get_component(SpriteRenderer2D).flip_x = True
                self._parent.get_component(Rigidbody2D).velocity = Vector2(-self.__speed_x, self._parent.get_component(Rigidbody2D).velocity.y)
                self._parent.get_component(SpriteAnimator2D).set_active_take(ActiveTake.PLAYER_WALKING)

    def _move_right(self):
        if self.__input_handler.is_tap(pygame.K_RIGHT, self.__tap_threshold):
            self._parent.get_component(SpriteRenderer2D).flip_x = False
            self._parent.get_component(SpriteAnimator2D).set_active_take(ActiveTake.PLAYER_RUNNING)
            self._parent.get_component(Rigidbody2D).velocity = Vector2(self.__speed_x, self._parent.get_component(Rigidbody2D).velocity.y)

    def _move_up(self):
        if self.__input_handler.is_tap(pygame.K_UP, self.__tap_threshold):
                self._parent.get_component(SpriteRenderer2D).flip_y = True
                self._parent.get_component(Rigidbody2D).velocity = Vector2(self._parent.get_component(Rigidbody2D).velocity.x, -self.__speed_y)

    def _move_down(self):
        if self.__input_handler.is_tap(pygame.K_DOWN, self.__tap_threshold):
                self._parent.get_component(SpriteRenderer2D).flip_y = False
                self._parent.get_component(Rigidbody2D).velocity = Vector2(self._parent.get_component(Rigidbody2D).velocity.x, self.__speed_y)
