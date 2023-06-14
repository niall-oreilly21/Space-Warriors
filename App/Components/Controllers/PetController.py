import pygame
from pygame import Vector2

from App.Components.Controllers.PlayerController import PlayerController
from App.Constants.GameConstants import GameConstants
from Engine.GameObjects.Components.FollowController import FollowController
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.Enums.GameObjectEnums import GameObjectDirection


class PetController(FollowController):
    def __init__(self, name, target_object, speed):
        super().__init__(name, target_object)
        self.__total_elapsed_time = 0
        self.__total_time = 6000
        self.__animator = None
        self.__rend = None
        self.__speed = speed
        self.__rigidbody = None
        self.__adopted = False

    @property
    def adopted(self):
        return self.__adopted

    def adopt(self):
        self.target.attack_damage += 3
        self.__adopted = True

    def start(self):
        self.__rend = self._parent.get_component(SpriteRenderer2D)
        self.__animator = self._parent.get_component(SpriteAnimator2D)
        self.__rigidbody = self._parent.get_component(Rigidbody2D)

    def update(self, game_time):
        if self.__adopted:
            self.__dog_bark(game_time)
            self._follow_target()

    def _follow_target(self):
        target_position = self.target.transform.position
        current_position = self._transform.position

        # Calculate the direction vector towards the target
        direction = target_position - current_position

        # Normalize the direction vector
        if direction.length() > 0:
            direction.normalize()

        self.__rigidbody.velocity = direction * self.__speed * 0.0001

        target_previous_direction = self.target.get_component(PlayerController).previous_direction
        if target_previous_direction == GameObjectDirection.Left:
            self.__rend.flip_x = True
        elif target_previous_direction == GameObjectDirection.Right:
            self.__rend.flip_x = False

        self.__animator.set_active_take(ActiveTake.PET_DOG_WALK)

        distance_from_target = 65

        target_active_take = self.target.get_component(SpriteAnimator2D).active_take

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

    def __dog_bark(self, game_time):
        self.__total_elapsed_time += game_time.elapsed_time

        if self.__total_elapsed_time >= self.__total_time:
            self.__total_elapsed_time = 0
            GameConstants.EVENT_DISPATCHER.dispatch_event(
                EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                          ["Your dog loves you! <3",
                           GameConstants.UITextPrompts.UI_TEXT_RIGHT]))
            GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SoundManager, EventActionType.PlaySound,[GameConstants.Music.DOG_BARK_SOUND, False]))




