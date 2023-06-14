import random
import time

import pygame
from pygame import Vector2

from App.Components.Controllers.PetController import PetController
from App.Components.Controllers.PlayerController import PlayerController
from App.Constants.Application import Application
from App.Constants.GameConstants import GameConstants
from Engine.GameObjects.Character import Character
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Collider import Collider
from Engine.GameObjects.PowerUp import PowerUp
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.Enums.GameObjectEnums import GameObjectCategory, PowerUpType


class PlayerCollider(Collider):
    def __init__(self, name):
        super().__init__(name)

    def show_text(self, colliding_game_object, power_up_type):
        # Show power up text
        symbol = ""
        if colliding_game_object.power_up_value >= 0:
            symbol = "+"

        type_str = "Health"
        if power_up_type == PowerUpType.Speed:
            type_str = "Speed"
        elif power_up_type == PowerUpType.Attack:
            type_str = "Attack damage"
        elif power_up_type == PowerUpType.Defense:
            type_str = "Defense"

        ui_text = type_str + " " + symbol + str(colliding_game_object.power_up_value)

        if power_up_type == PowerUpType.NightVision:
            ui_text = "Night vision on"

        GameConstants.EVENT_DISPATCHER.dispatch_event(
            EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                      [ui_text, GameConstants.UITextPrompts.UI_TEXT_RIGHT]))
        self.__text_shown = True
        self.__text_shown_time = 0

    def handle_response(self, colliding_game_object):
        current_time = time.time()

        # Player and enemy collide
        if self._is_colliding_with_enemy(colliding_game_object):

            # Player take damage
            if current_time - self.parent.last_damage_time >= self.parent.damage_cooldown:
                self.parent.is_damaged = True
                self.parent.damage(colliding_game_object.attack_damage)
                self.parent.last_damage_time = current_time

            else:
                self.parent.is_damaged = False

            # Enemy take damage
            player_active_take = self.parent.get_component(SpriteAnimator2D).active_take
            if player_active_take == ActiveTake.PLAYER_ATTACK_X or \
                    player_active_take == ActiveTake.PLAYER_ATTACK_UP or \
                    player_active_take == ActiveTake.PLAYER_ATTACK_DOWN:
                if current_time - colliding_game_object.last_damage_time >= colliding_game_object.damage_cooldown:
                    colliding_game_object.is_damaged = True
                    colliding_game_object.damage(self.parent.attack_damage)
                    colliding_game_object.last_damage_time = current_time
                else:
                    colliding_game_object.is_damaged = False

        # Player and pet collide
        if colliding_game_object.game_object_category == GameObjectCategory.Pet:
            GameConstants.EVENT_DISPATCHER.dispatch_event(
                EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                          ["You found a stranded dog! Press E to adopt", GameConstants.UITextPrompts.UI_TEXT_BOTTOM]))
            if GameConstants.INPUT_HANDLER.is_tap(pygame.K_e, 100):
                GameConstants.EVENT_DISPATCHER.dispatch_event(
                    EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                              ["",
                               GameConstants.UITextPrompts.UI_TEXT_BOTTOM]))
                GameConstants.EVENT_DISPATCHER.dispatch_event(
                    EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                              ["Attack damage +3",
                               GameConstants.UITextPrompts.UI_TEXT_RIGHT]))
                GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SoundManager, EventActionType.PlaySound,[GameConstants.Music.DOG_BARK_SOUND, False]))

                colliding_game_object.get_component(PetController).adopt()

                GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.CollisionManager, EventActionType.RemoveColliderFromQuadTree, [colliding_game_object.get_component(BoxCollider2D)]))

                colliding_game_object.remove_component(BoxCollider2D)

