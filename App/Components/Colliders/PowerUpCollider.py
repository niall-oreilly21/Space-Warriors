import random

import pygame
from pygame import Vector2

from App.Components.Controllers.PlayerController import PlayerController
from App.Constants.Application import Application
from App.Constants.GameConstants import GameConstants
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Collider import Collider
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Other.Enums.EventEnums import EventActionType, EventCategoryType
from Engine.Other.Enums.GameObjectEnums import PowerUpType


class PowerUpCollider(Collider):
    def __init__(self, name, min_power_up_value, max_power_up_value, __prompt_text):
        super().__init__(name)
        self.__current_elapsed_time = 0
        self.__text_shown_time = 0
        self.__text_shown = False

        self.__power_up_activated = False
        self.__text_time = 10000
        self.__total_time = 10000
        self.__min_power_up_value = min_power_up_value
        self.__max_power_up_value = max_power_up_value
        self.__prompt_text = __prompt_text

    def handle_response(self, colliding_game_object):
        if colliding_game_object == Application.Player:
            if self.parent.power_up_type is PowerUpType.Random:
                GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,[self.__prompt_text, GameConstants.UITextPrompts.UI_TEXT_BOTTOM]))

                random_type = random.choice([PowerUpType.Heal, PowerUpType.Speed, PowerUpType.Attack, PowerUpType.Defense])

                if random_type == PowerUpType.Heal:
                    self._parent.power_up_value = min(random.randint(-8, 10), random.randint(-8, 10))
                else:
                    self._parent.power_up_value = min(random.randint(-3, 3), random.randint(-3, 3))

                self.__handle_power_up_selected(colliding_game_object, random_type)
            else:
                self.__handle_power_up_collision()
                self.__handle_power_up_selected(colliding_game_object, self._parent.power_up_type)


    def __handle_power_up_collision(self):
        self.parent.power_up_value = random.randint(self.__max_power_up_value, self.__max_power_up_value)
        GameConstants.EVENT_DISPATCHER.dispatch_event(
            EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper, [self.__prompt_text, GameConstants.UITextPrompts.UI_TEXT_BOTTOM]))

    def __handle_power_up_selected(self, player, power_up_type):
        if GameConstants.INPUT_HANDLER.is_tap(pygame.K_e, 100):
            self.__power_up_activated = True

            GameConstants.EVENT_DISPATCHER.dispatch_event(
                EventData(EventCategoryType.SoundManager, EventActionType.PlaySound,
                          [GameConstants.Music.POTION_DRINK_SOUND, None]))

            if power_up_type == PowerUpType.Heal:
                player.health += self.parent.power_up_value
                self.show_text(PowerUpType.Heal)

            elif power_up_type == PowerUpType.Defense:
                player.damage_cooldown += self.parent.power_up_value
                self.show_text(PowerUpType.Defense)

            elif power_up_type == PowerUpType.Attack:
                player.attack_damage += self.parent.power_up_value
                self.show_text(PowerUpType.Attack)

            elif power_up_type == PowerUpType.Speed:
                player.get_component(SpriteAnimator2D).fps += self.parent.power_up_value
                player_speed_x = player.get_component(PlayerController).speed.x
                player_speed_y = player.get_component(PlayerController).speed.y
                player.get_component(PlayerController).speed = Vector2(
                    player_speed_x + self.parent.power_up_value * 0.01,
                    player_speed_y + self.parent.power_up_value * 0.01)
                self.show_text(PowerUpType.Speed)

            else:
                GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.RendererManager,
                                                                        EventActionType.TurnSpotLightOff))
                self.show_text(PowerUpType.NightVision)

            Application.ActiveScene.dispatch_quad_tree_remove_events(self.parent)

            self.parent.remove_component(Renderer2D)
            self.parent.remove_component(BoxCollider2D)


    def show_text(self, power_up_type):
        # Show power up text
        symbol = ""
        if self.parent.power_up_value >= 0:
            symbol = "+"

        type_str = "Health"
        if power_up_type == PowerUpType.Speed:
            type_str = "Speed"
        elif power_up_type == PowerUpType.Attack:
            type_str = "Attack damage"
        elif power_up_type == PowerUpType.Defense:
            type_str = "Defense"

        ui_text = type_str + " " + symbol + str(self.parent.power_up_value)

        if power_up_type == PowerUpType.NightVision:
            ui_text = "Night vision on"

        GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,["", GameConstants.UITextPrompts.UI_TEXT_BOTTOM]))

        GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper, [ui_text, GameConstants.UITextPrompts.UI_TEXT_RIGHT]))
        self.__text_shown = True
        self.__text_shown_time = 0

    def update(self, game_time):

        # Power up activation
        if self.__power_up_activated:
            self.__current_elapsed_time += game_time.elapsed_time

            if self.__current_elapsed_time >= self.__total_time:
                self.__current_elapsed_time = 0

                if self.parent.power_up_type is PowerUpType.Attack:
                        Application.Player.attack_damage = GameConstants.Player.DEFAULT_ATTACK_DAMAGE

                elif self.parent.power_up_type is PowerUpType.Defense:
                        Application.Player.damage_cooldown = GameConstants.Player.DAMAGE_COOLDOWN

                elif self.parent.power_up_type is PowerUpType.Speed:
                        Application.Player.get_component(PlayerController).speed = Vector2(GameConstants.Player.MOVE_SPEED, GameConstants.Player.MOVE_SPEED)

                        Application.Player.get_component(SpriteAnimator2D).fps = GameConstants.CHARACTER_ANIMATOR_MOVE_SPEED

                elif self.parent.power_up_type is PowerUpType.NightVision:

                        GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.RendererManager, EventActionType.TurnSpotLightOn))

                if Application.ActiveScene.contains(self.parent):
                    Application.ActiveScene.remove(self.parent)

        if self.__text_shown:
            self.__text_shown_time += game_time.elapsed_time
            if self.__text_shown_time >= self.__text_time:
                self.__text_shown_time = 0
                self.__text_shown = False

    def handle_collision_exit(self):
        GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper, ["", GameConstants.UITextPrompts.UI_TEXT_BOTTOM]))
        GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,["", GameConstants.UITextPrompts.UI_TEXT_RIGHT]))

    def clone(self):
        return PowerUpCollider(self.name, self.__min_power_up_value, self.__max_power_up_value, self.__prompt_text)
