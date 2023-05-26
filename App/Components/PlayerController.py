from pygame import Vector2

from Engine.GameObjects.Components.Component import Component
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Other.Enums import GameObjectEnums
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.InputHandler import InputHandler
from Engine.Other.Interfaces.IMoveable import IMoveable
import pygame


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
        self.__is_moving = False
        self.__previous_direction = None

    def start(self):
        self.__rb = self._parent.get_component(Rigidbody2D)
        self.__rend = self._parent.get_component(SpriteRenderer2D)
        self.__animator = self._parent.get_component(SpriteAnimator2D)

    def update(self, game_time):
        # self.transform.rotate(0.1 * game_time.elapsed_time)

        self.__rb.velocity = Vector2(0, 0)
        self.__input_handler.update()
        self._move_left()
        self._move_right()
        self._move_up()
        self._move_down()
        self._attack()

    def _move_left(self):
        self._set_idle_animation()
        if self.__input_handler.is_tap(pygame.K_a, self.__tap_threshold):
            self.__rend.flip_x = True
            self.__rb.velocity = Vector2(-self.__speed_x, self.__rb.velocity.y)
            self.__animator.set_active_take(ActiveTake.PLAYER_MOVE_X)
            self.__is_moving = True
            self.__previous_direction = GameObjectEnums.GameObjectDirection.Left

    def _move_right(self):
        self._set_idle_animation()
        if self.__input_handler.is_tap(pygame.K_d, self.__tap_threshold):
            self.__rend.flip_x = False
            self.__animator.set_active_take(ActiveTake.PLAYER_MOVE_X)
            self.__rb.velocity = Vector2(self.__speed_x, self.__rb.velocity.y)
            self.__is_moving = True
            self.__previous_direction = GameObjectEnums.GameObjectDirection.Right

    def _move_up(self):
        self._set_idle_animation()
        if self.__input_handler.is_tap(pygame.K_w, self.__tap_threshold):
            self.__rend.flip_y = False
            self.__rb.velocity = Vector2(self.__rb.velocity.x, -self.__speed_y)
            self.__animator.set_active_take(ActiveTake.PLAYER_MOVE_UP)
            self.__is_moving = True
            self.__previous_direction = GameObjectEnums.GameObjectDirection.Up

    def _move_down(self):
        self._set_idle_animation()
        if self.__input_handler.is_tap(pygame.K_s, self.__tap_threshold):
            self.__rend.flip_y = False
            self.__rb.velocity = Vector2(self.__rb.velocity.x, self.__speed_y)
            self.__animator.set_active_take(ActiveTake.PLAYER_MOVE_DOWN)
            self.__is_moving = True
            self.__previous_direction = GameObjectEnums.GameObjectDirection.Down

    def _set_idle_animation(self):
        if not self.__input_handler.is_tap(pygame.K_w, self.__tap_threshold) \
                and not self.__input_handler.is_tap(pygame.K_a, self.__tap_threshold) \
                and not self.__input_handler.is_tap(pygame.K_s, self.__tap_threshold) \
                and not self.__input_handler.is_tap(pygame.K_d, self.__tap_threshold):
            self.__is_moving = False
        if not self.__is_moving:
            if self.__previous_direction == GameObjectEnums.GameObjectDirection.Left \
                    or self.__previous_direction == GameObjectEnums.GameObjectDirection.Right:
                self.__animator.set_active_take(ActiveTake.PLAYER_IDLE_X)
            elif self.__previous_direction == GameObjectEnums.GameObjectDirection.Up:
                self.__animator.set_active_take(ActiveTake.PLAYER_IDLE_UP)
            elif self.__previous_direction == GameObjectEnums.GameObjectDirection.Down:
                self.__animator.set_active_take(ActiveTake.PLAYER_IDLE_DOWN)

    def _attack(self):
        if pygame.mouse.get_pressed()[0]:
            if self.__previous_direction == GameObjectEnums.GameObjectDirection.Left \
                    or self.__previous_direction == GameObjectEnums.GameObjectDirection.Right:
                self.__animator.set_active_take(ActiveTake.PLAYER_ATTACK_X)
            elif self.__previous_direction == GameObjectEnums.GameObjectDirection.Up:
                self.__animator.set_active_take(ActiveTake.PLAYER_ATTACK_UP)
            elif self.__previous_direction == GameObjectEnums.GameObjectDirection.Down:
                self.__animator.set_active_take(ActiveTake.PLAYER_ATTACK_DOWN)
