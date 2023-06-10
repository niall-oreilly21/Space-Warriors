import random
import time

import pygame
from pygame import Vector2

from App.Components.Controllers.PetController import PetController
from App.Components.Controllers.PlayerController import PlayerController
from App.Constants.Application import Application
from App.Constants.Constants import Constants
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


def handle_power_up_collision(colliding_game_object: PowerUp, min_value, max_value, prompt_text):
    colliding_game_object.power_up_value = random.randint(min_value, max_value)
    Constants.EVENT_DISPATCHER.dispatch_event(
        EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                  [prompt_text, Constants.UITextPrompts.UI_TEXT_BOTTOM]))


class PlayerCollider(Collider):
    def __init__(self, name):
        super().__init__(name)
        self.__current_speed_time = 0
        self.__current_attack_time = 0
        self.__current_defense_time = 0

        self.__text_shown_time = 0
        self.__text_shown = False

        self.__speed_activated = False
        self.__attack_activated = False
        self.__defense_activated = False

        self.__text_time = 10000
        self.__total_time = 10000

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
        Constants.EVENT_DISPATCHER.dispatch_event(
            EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                      [ui_text, Constants.UITextPrompts.UI_TEXT_RIGHT]))
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
                print("Health: ", self.parent.health)
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
                    print("Enemy health: ", colliding_game_object.health)
                else:
                    colliding_game_object.is_damaged = False

            # if self.parent.health == 0:
            #     self.parent.health = Constants.Player.DEFAULT_HEALTH


        # Player and power up collide
        if isinstance(colliding_game_object, PowerUp):
            if colliding_game_object.power_up_type == PowerUpType.Heal:
                handle_power_up_collision(colliding_game_object, 5, 15, "Press E to heal")
                self.handle_power_up_selected(self.parent, colliding_game_object, PowerUpType.Heal)
            elif colliding_game_object.power_up_type == PowerUpType.Attack:
                handle_power_up_collision(colliding_game_object, 1, 5, "Press E to increase attack damage")
                self.handle_power_up_selected(self.parent, colliding_game_object, PowerUpType.Attack)
            elif colliding_game_object.power_up_type == PowerUpType.Defense:
                handle_power_up_collision(colliding_game_object, 1, 5, "Press E to increase defense")
                self.handle_power_up_selected(self.parent, colliding_game_object, PowerUpType.Defense)
            elif colliding_game_object.power_up_type == PowerUpType.Speed:
                handle_power_up_collision(colliding_game_object, 1, 5, "Press E to increase speed")
                self.handle_power_up_selected(self.parent, colliding_game_object, PowerUpType.Speed)
            else:
                Constants.EVENT_DISPATCHER.dispatch_event(
                    EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                              ["Press E to get a random power up", Constants.UITextPrompts.UI_TEXT_BOTTOM]))
                random_type = random.choice([PowerUpType.Heal, PowerUpType.Speed, PowerUpType.Attack,
                                             PowerUpType.Defense])
                if random_type == PowerUpType.Heal:
                    colliding_game_object.power_up_value = min(random.randint(-8, 10), random.randint(-8, 10))
                else:
                    colliding_game_object.power_up_value = min(random.randint(-3, 3), random.randint(-3, 3))

                self.handle_power_up_selected(self.parent, colliding_game_object, random_type)

        # Player and pet collide
        if colliding_game_object.game_object_category == GameObjectCategory.Pet:
            Constants.EVENT_DISPATCHER.dispatch_event(
                EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                          ["You found a stranded dog! Press E to adopt", Constants.UITextPrompts.UI_TEXT_BOTTOM]))
            if Constants.INPUT_HANDLER.is_tap(pygame.K_e, 100):
                colliding_game_object.get_component(PetController).adopt()

                Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.CollisionManager, EventActionType.RemoveColliderFromQuadTree, [colliding_game_object.get_component(BoxCollider2D)]))

                colliding_game_object.remove_component(BoxCollider2D)
                Constants.EVENT_DISPATCHER.dispatch_event(
                    EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                              ["Your dog loves you <3!",
                               Constants.UITextPrompts.UI_TEXT_RIGHT]))
                self.__text_shown = True
                self.__text_shown_time = 0
                Constants.EVENT_DISPATCHER.dispatch_event(
                    EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                              ["He will help you in battles and heal you every 30 secs!",
                               Constants.UITextPrompts.UI_TEXT_RIGHT]))
                self.__text_shown = True
                self.__text_shown_time = 0
                Constants.EVENT_DISPATCHER.dispatch_event(
                    EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                              ["Attack damage +3",
                               Constants.UITextPrompts.UI_TEXT_RIGHT]))
                self.__text_shown = True
                self.__text_shown_time = 0

    def handle_power_up_selected(self, player: Character, colliding_game_object: PowerUp, power_up_type: PowerUpType):
        if Constants.INPUT_HANDLER.is_tap(pygame.K_e, 100):
            Constants.EVENT_DISPATCHER.dispatch_event(
                EventData(EventCategoryType.SoundManager, EventActionType.PlaySound,
                          [Constants.Music.POTION_DRINK_SOUND, None]))
            if power_up_type == PowerUpType.Heal:
                player.health += colliding_game_object.power_up_value
                self.show_text(colliding_game_object, PowerUpType.Heal)
            elif power_up_type == PowerUpType.Defense:
                player.damage_cooldown += colliding_game_object.power_up_value
                self.__defense_activated = True
                self.show_text(colliding_game_object, PowerUpType.Defense)
            elif power_up_type == PowerUpType.Attack:
                player.attack_damage += colliding_game_object.power_up_value
                self.__attack_activated = True
                self.show_text(colliding_game_object, PowerUpType.Attack)
            elif power_up_type == PowerUpType.Speed:
                player_speed_x = player.get_component(PlayerController).speed.x
                player_speed_y = player.get_component(PlayerController).speed.y
                player.get_component(PlayerController).speed = Vector2(
                    player_speed_x + colliding_game_object.power_up_value * 0.01,
                    player_speed_y + colliding_game_object.power_up_value * 0.01)
                self.__speed_activated = True
                self.show_text(colliding_game_object, PowerUpType.Speed)

            if Application.ActiveScene.contains(colliding_game_object):
                Application.ActiveScene.remove(colliding_game_object)

            Constants.EVENT_DISPATCHER.dispatch_event(
                EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                          ["", Constants.UITextPrompts.UI_TEXT_BOTTOM]))


    def update(self, game_time):
        # Power up activation
        if self.__attack_activated:
            self.__current_attack_time += game_time.elapsed_time
            if self.__current_attack_time >= self.__total_time:
                self.__current_attack_time = 0
                self.__attack_activated = False
                self.parent.attack_damage = Constants.Player.DEFAULT_ATTACK_DAMAGE

        if self.__defense_activated:
            self.__current_defense_time += game_time.elapsed_time
            if self.__current_defense_time >= self.__total_time:
                self.__current_defense_time = 0
                self.__defense_activated = False
                self.parent.damage_cooldown = Constants.Player.DAMAGE_COOLDOWN

        if self.__speed_activated:
            self.__current_speed_time += game_time.elapsed_time
            if self.__current_speed_time >= self.__total_time:
                self.__current_speed_time = 0
                self.__speed_activated = False
                self.parent.get_component(PlayerController).speed = Vector2(Constants.Player.MOVE_SPEED,
                                                                            Constants.Player.MOVE_SPEED)

        # Show power up text
        if self.__text_shown:
            self.__text_shown_time += game_time.elapsed_time
            if self.__text_shown_time >= self.__text_time:
                self.__text_shown_time = 0
                self.__text_shown = False
                Constants.EVENT_DISPATCHER.dispatch_event(
                    EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                              ["", Constants.UITextPrompts.UI_TEXT_RIGHT]))
