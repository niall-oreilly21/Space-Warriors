from pygame import Vector2

from App.Components.Colliders.AttackBoxCollider2D import AttackBoxCollider2D
from App.Constants.Constants import Constants
from Engine.GameObjects.Components.Component import Component
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Managers.SceneManager import SceneManager
from Engine.Other.Enums import GameObjectEnums
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.InputHandler import InputHandler
from Engine.Other.Interfaces.IMoveable import IMoveable
import pygame


class PlayerController(Component, IMoveable):

    def __init__(self, name, speed_x, speed_y, box_collider):
        super().__init__(name)
        self.__input_handler = InputHandler()
        self.__speed_x = speed_x
        self.__speed_y = speed_y
        self.__tap_threshold = 100
        self.__animator = None
        self.__rb = None
        self.__rend = None
        self.__is_moving = False
        self.__is_attacking = False
        self.__previous_direction = GameObjectEnums.GameObjectDirection.Down
        self.__box_collider = box_collider

    @property
    def previous_direction(self):
        return self.__previous_direction

    @property
    def input_handler(self):
        return self.__input_handler

    @property
    def speed(self):
        return Vector2(self.__speed_x, self.__speed_y)

    @speed.setter
    def speed(self, speed):
        self.__speed_x = speed.x
        self.__speed_y = speed.y

    def start(self):
        self.__rb = self._parent.get_component(Rigidbody2D)
        self.__rend = self._parent.get_component(SpriteRenderer2D)
        self.__animator = self._parent.get_component(SpriteAnimator2D)

    def update(self, game_time):
        self.__rb.velocity = Vector2(0, 0)

        if self.__animator.active_take == ActiveTake.PLAYER_ATTACK_X \
                or self.__animator.active_take == ActiveTake.PLAYER_ATTACK_UP\
                or self.__animator.active_take == ActiveTake.PLAYER_ATTACK_DOWN:
            if not self.__animator.is_animation_complete:
                # Animation is still playing, stop movement
                return
        else:
            # Animation is complete, switch to the next take
            self._set_idle_animation()

        self.__input_handler.update()
        self._move_left()
        self._move_right()
        self._move_up()
        self._move_down()
        self._attack()
        self._faint()
        #
        # if self.parent.is_damaged:
        #     self.parent.get_component(Renderer2D).material.alpha = 150
        # else:
        #     self.parent.get_component(Renderer2D).material.alpha = 225

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
        if self.__previous_direction == GameObjectEnums.GameObjectDirection.Up:
            attack_key = pygame.K_UP
        elif self.__previous_direction == GameObjectEnums.GameObjectDirection.Down:
            attack_key = pygame.K_DOWN
        elif self.__previous_direction == GameObjectEnums.GameObjectDirection.Left:
            attack_key = pygame.K_LEFT
        else:
            attack_key = pygame.K_RIGHT

        if self.__input_handler.is_tap(attack_key, self.__tap_threshold):
            self.parent.remove_component(BoxCollider2D)

            self.__is_attacking = True
            Constants.EVENT_DISPATCHER.dispatch_event(
                EventData(EventCategoryType.SoundManager, EventActionType.PlaySound, ["AttackSound"]))
            attack_collider = AttackBoxCollider2D("Attack box collider", self)
            self.parent.add_component(attack_collider)

            if self.__previous_direction == GameObjectEnums.GameObjectDirection.Left \
                    or self.__previous_direction == GameObjectEnums.GameObjectDirection.Right:
                self.__animator.set_active_take(ActiveTake.PLAYER_ATTACK_X)
            elif self.__previous_direction == GameObjectEnums.GameObjectDirection.Up:
                self.__animator.set_active_take(ActiveTake.PLAYER_ATTACK_UP)
            elif self.__previous_direction == GameObjectEnums.GameObjectDirection.Down:
                self.__animator.set_active_take(ActiveTake.PLAYER_ATTACK_DOWN)
        else:
            self.__is_attacking = False
            if self.parent.get_component(AttackBoxCollider2D):
                self.parent.remove_component(AttackBoxCollider2D)
                self.parent.add_component(self.__box_collider)

    def _faint(self):

        if self.parent.health <= 0:
            print("FAINT")
            self.__animator.set_active_take(ActiveTake.PLAYER_IDLE_DOWN)
            Constants.EVENT_DISPATCHER.dispatch_event(
                EventData(EventCategoryType.SceneManager, EventActionType.DeathScene))

