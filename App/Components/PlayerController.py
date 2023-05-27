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
        self.__animator = None
        self.__rb = None
        self.__rend = None

    def start(self):
        self.__rb = self._parent.get_component(Rigidbody2D)
        self.__rend = self._parent.get_component(SpriteRenderer2D)
        self.__animator = self._parent.get_component(SpriteAnimator2D)

    def update(self, game_time):
        self._parent.get_component(Rigidbody2D).velocity = Vector2(0, 0)

        self._parent.transform.rotate(5)
        # if self.__animator.active_take == ActiveTake.COOK:
        #     if not self.__animator.is_animation_complete:
        #         # Animation is still playing, stop movement
        #         return
        # else:
        #     # Animation is complete, switch to the next take
        #     self.__animator.set_active_take(ActiveTake.PLAYER_WALKING)

        self.__input_handler.update()
        self._move_left()
        self._move_right()
        self._move_up()
        self._move_down()

    def _move_left(self):
        if self.__input_handler.is_tap(pygame.K_LEFT, self.__tap_threshold):
                self.__rend.flip_x = True
                self.__rb.velocity = Vector2(-self.__speed_x, self.__rb.velocity.y)
                self.__animator.set_active_take(ActiveTake.PLAYER_WALKING)

    def _move_right(self):
        if self.__input_handler.is_tap(pygame.K_RIGHT, self.__tap_threshold):
            self.__rend.flip_x = False
            self.__animator.set_active_take(ActiveTake.PLAYER_RUNNING)
            self.__rb.velocity = Vector2(self.__speed_x, self.__rb.velocity.y)

    def _move_up(self):
        if self.__input_handler.is_tap(pygame.K_UP, self.__tap_threshold):
                self.__rend.flip_y = True
                self.__rb.velocity = Vector2(self.__rb.velocity.x, -self.__speed_y)

    def _move_down(self):
        if self.__input_handler.is_tap(pygame.K_DOWN, self.__tap_threshold):
                self.__rend.flip_y = False
                self.__rb.velocity = Vector2(self.__rb.velocity.x, self.__speed_y)

    def clone(self):
        pass