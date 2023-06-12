import random

import pygame
from pygame import Vector2

from App.Components.Controllers.PlayerController import PlayerController
from App.Constants.Application import Application
from App.Constants.GameConstants import GameConstants
from Engine.GameObjects.Components.Physics.Collider import Collider
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Other.Enums.EventEnums import EventActionType, EventCategoryType
from Engine.Other.Enums.GameObjectEnums import PowerUpType


class PowerUpCollider(Collider):
    def __init__(self, name):
        super().__init__(name)
        self.__current_speed_time = 0
        self.__current_attack_time = 0
        self.__current_defense_time = 0
        self.__current_night_vision_time = 0

        self.__text_shown_time = 0
        self.__text_shown = False

        self.__speed_activated = False
        self.__attack_activated = False
        self.__defense_activated = False
        self.__night_vision_activated = False

        self.__text_time = 10000
        self.__total_time = 10000

    def handle_response(self, colliding_game_object):
        if colliding_game_object == Application.Player:
            if self.parent.power_up_type == PowerUpType.Heal:
                self.__handle_power_up_collision(5, 15, "Press E to heal")
                self.__handle_power_up_selected(colliding_game_object, PowerUpType.Heal)

            elif self.parent.power_up_type == PowerUpType.Attack:
                self.__handle_power_up_collision(1, 5, "Press E to increase attack damage")
                self.__handle_power_up_selected(colliding_game_object, PowerUpType.Attack)

            elif self.parent.power_up_type == PowerUpType.Defense:
                self.__handle_power_up_collision(1, 5, "Press E to increase defense")
                self.__handle_power_up_selected(colliding_game_object, PowerUpType.Defense)

            elif self.parent.power_up_type == PowerUpType.Speed:
                self.__handle_power_up_collision(1, 5, "Press E to increase speed")
                self.__handle_power_up_selected(colliding_game_object, PowerUpType.Speed)

            elif self.parent.power_up_type == PowerUpType.NightVision:
                self.__handle_power_up_collision(0, 0, "Press E to equip night vision goggles")
                self.__handle_power_up_selected(colliding_game_object, PowerUpType.NightVision)

            else:
                GameConstants.EVENT_DISPATCHER.dispatch_event(
                    EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                              ["Press E to get a random power up", GameConstants.UITextPrompts.UI_TEXT_BOTTOM]))
                random_type = random.choice([PowerUpType.Heal, PowerUpType.Speed, PowerUpType.Attack,
                                             PowerUpType.Defense])
                if random_type == PowerUpType.Heal:
                    colliding_game_object.power_up_value = min(random.randint(-8, 10), random.randint(-8, 10))
                else:
                    colliding_game_object.power_up_value = min(random.randint(-3, 3), random.randint(-3, 3))

                self.__handle_power_up_selected(colliding_game_object, random_type)

    def __handle_power_up_collision(self, min_value, max_value, prompt_text):
        self.parent.power_up_value = random.randint(min_value, max_value)
        GameConstants.EVENT_DISPATCHER.dispatch_event(
            EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper, [prompt_text, GameConstants.UITextPrompts.UI_TEXT_BOTTOM]))

    def __handle_power_up_selected(self, player, power_up_type: PowerUpType):
        if GameConstants.INPUT_HANDLER.is_tap(pygame.K_e, 100):
            GameConstants.EVENT_DISPATCHER.dispatch_event(
                EventData(EventCategoryType.SoundManager, EventActionType.PlaySound,
                          [GameConstants.Music.POTION_DRINK_SOUND, None]))

            if power_up_type == PowerUpType.Heal:
                player.health += self.parent.power_up_value
                self.show_text(PowerUpType.Heal)

            elif power_up_type == PowerUpType.Defense:
                player.damage_cooldown += self.parent.power_up_value
                self.__defense_activated = True
                self.show_text(PowerUpType.Defense)

            elif power_up_type == PowerUpType.Attack:
                player.attack_damage += self.parent.power_up_value
                self.__attack_activated = True
                self.show_text(PowerUpType.Attack)

            elif power_up_type == PowerUpType.Speed:
                print("Yes")
                player.get_component(SpriteAnimator2D).fps += self.parent.power_up_value
                player_speed_x = player.get_component(PlayerController).speed.x
                player_speed_y = player.get_component(PlayerController).speed.y
                player.get_component(PlayerController).speed = Vector2(
                    player_speed_x + self.parent.power_up_value * 0.01,
                    player_speed_y + self.parent.power_up_value * 0.01)
                self.__speed_activated = True
                self.show_text(PowerUpType.Speed)

            else:
                GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.RendererManager,
                                                                        EventActionType.TurnSpotLightOff))
                self.__night_vision_activated = True
                self.show_text(PowerUpType.NightVision)

            if Application.ActiveScene.contains(self.parent):
                Application.ActiveScene.remove(self.parent)

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

        GameConstants.EVENT_DISPATCHER.dispatch_event(
            EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                      [ui_text, GameConstants.UITextPrompts.UI_TEXT_RIGHT2]))
        self.__text_shown = True
        self.__text_shown_time = 0

    def handle_collision_exit(self):
        GameConstants.EVENT_DISPATCHER.dispatch_event(
            EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                      ["", GameConstants.UITextPrompts.UI_TEXT_BOTTOM]))
        GameConstants.EVENT_DISPATCHER.dispatch_event(
            EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                      ["", GameConstants.UITextPrompts.UI_TEXT_RIGHT2]))

    def clone(self):
        return PowerUpCollider(self.name)

    def update(self, game_time):
        #print(self.__speed_activated)
        # Power up activation
        if self.__attack_activated:
            self.__current_attack_time += game_time.elapsed_time
            if self.__current_attack_time >= self.__total_time:
                self.__current_attack_time = 0
                self.__attack_activated = False
                Application.Player.attack_damage = GameConstants.Player.DEFAULT_ATTACK_DAMAGE

        if self.__defense_activated:
            self.__current_defense_time += game_time.elapsed_time
            if self.__current_defense_time >= self.__total_time:
                self.__current_defense_time = 0
                self.__defense_activated = False
                Application.Player.damage_cooldown = GameConstants.Player.DAMAGE_COOLDOWN

        if self.__speed_activated:
            print("im sonic zip zip")
            print(Application.Player.get_component(PlayerController).speed)
            self.__current_speed_time += game_time.elapsed_time
            if self.__current_speed_time >= self.__total_time:
                self.__current_speed_time = 0
                self.__speed_activated = False
                Application.Player.get_component(PlayerController).speed = Vector2(GameConstants.Player.MOVE_SPEED,
                                                                            GameConstants.Player.MOVE_SPEED)
                print(Application.Player.get_component(PlayerController).speed)
                Application.Player.get_component(SpriteAnimator2D).fps = GameConstants.CHARACTER_ANIMATOR_MOVE_SPEED

        if self.__night_vision_activated:
            self.__current_night_vision_time += game_time.elapsed_time
            if self.__current_night_vision_time >= self.__total_time:
                self.__current_night_vision_time = 0
                self.__night_vision_activated = False
                GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.RendererManager,
                                                                        EventActionType.TurnSpotLightOn))

        # Show power up text
        if self.__text_shown:
            self.__text_shown_time += game_time.elapsed_time
            if self.__text_shown_time >= self.__text_time:
                self.__text_shown_time = 0
                self.__text_shown = False
