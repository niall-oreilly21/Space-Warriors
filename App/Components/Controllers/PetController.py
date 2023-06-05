import pygame
from pygame import Vector2

from App.Components.Controllers import PlayerController
from Engine.GameObjects.Components.Component import Component
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Enums.GameObjectEnums import GameObjectDirection


class PetController(Component):
    def __init__(self, name, target_object, speed):
        super().__init__(name)
        self.__animator = None
        self.__rend = None
        self.__target_object = target_object
        self.__speed = speed
        self.__rigidbody = None
        self.__adopted = False

    @property
    def adopted(self):
        return self.__adopted

    def __adopt(self):
            self.__adopted = True

    def start(self):
        self.__rend = self._parent.get_component(SpriteRenderer2D)
        self.__animator = self._parent.get_component(SpriteAnimator2D)
        self.__rigidbody = self._parent.get_component(Rigidbody2D)

    def update(self, game_time):
        target_position = self.__target_object.transform.position
        current_position = self._transform.position

        # Calculate the direction vector towards the target
        direction = target_position - current_position

        # Normalize the direction vector
        if direction.length() > 0:
            direction.normalize()

        if direction.length() <= 70:
            if self.__target_object.get_component(PlayerController).input_handler.is_tap(pygame.K_e, 200):
                self.__adopt()

        if self.__adopted:
            self.__rigidbody.velocity = direction * self.__speed * 0.0001

            target_previous_direction = self.__target_object.get_component(PlayerController).previous_direction
            if target_previous_direction == GameObjectDirection.Left:
                self.__rend.flip_x = True
            elif target_previous_direction == GameObjectDirection.Right:
                self.__rend.flip_x = False

            self.__animator.set_active_take(ActiveTake.PET_DOG_WALK)

            distance_from_target = 65

            target_active_take = self.__target_object.get_component(SpriteAnimator2D).active_take

            if target_active_take == ActiveTake.PLAYER_ATTACK_X and \
                    target_previous_direction == GameObjectDirection.Left:
                distance_from_target = 150
            elif target_active_take == ActiveTake.PLAYER_ATTACK_UP:
                distance_from_target = 100

            if direction.length() <= distance_from_target:
                self.__rigidbody.velocity = Vector2(0, 0)
                if target_active_take == ActiveTake.PLAYER_ATTACK_X or target_active_take == ActiveTake.PLAYER_ATTACK_UP \
                        or target_active_take == ActiveTake.PLAYER_ATTACK_DOWN:
                    self.__animator.set_active_take(ActiveTake.PET_DOG_IDLE)
                else:
                    self.__animator.set_active_take(ActiveTake.PET_DOG_SIT)
            else:
                # Calculate the movement amount based on speed and elapsed time
                movement_amount = self.__rigidbody.velocity = direction * self.__speed * 0.0001

                # Update the position
                self._transform.position += movement_amount
