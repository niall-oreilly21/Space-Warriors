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
                  [prompt_text]))


def handle_power_up_selected(player: Character, colliding_game_object: PowerUp, power_up_type: PowerUpType):
    if Constants.INPUT_HANDLER.is_tap(pygame.K_e, 100):
        if power_up_type == PowerUpType.Heal:
            player.health += colliding_game_object.power_up_value
        elif power_up_type == PowerUpType.Defense:
            player.damage_cooldown += colliding_game_object.power_up_value
        elif power_up_type == PowerUpType.Attack:
            player.attack_damage += colliding_game_object.power_up_value
        elif power_up_type == PowerUpType.Speed:
            player.get_component(PlayerController).speed = Vector2(colliding_game_object.power_up_value * 0.1,
                                                                   colliding_game_object.power_up_value * 0.1)

        Application.ActiveScene.remove(colliding_game_object)
        Constants.EVENT_DISPATCHER.dispatch_event(
            EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                      [""]))
        Constants.EVENT_DISPATCHER.dispatch_event(
            EventData(EventCategoryType.CollisionManager, EventActionType.RemoveCollliderFromQuadTree,
                      [colliding_game_object.get_component(BoxCollider2D)]))


class PlayerCollider(Collider):

    def __init__(self, name):
        super().__init__(name)

    def handle_response(self, colliding_game_object):
        current_time = time.time()

        # Player and enemy collide
        if colliding_game_object.game_object_category == GameObjectCategory.Alien or \
                colliding_game_object.game_object_category == GameObjectCategory.Wolf or \
                colliding_game_object.game_object_category == GameObjectCategory.Rat:

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

            if self.parent.health == 0:
                self.parent.health = Constants.Player.DEFAULT_HEALTH

            if colliding_game_object.health == 0:
                print("Enemy dead")
                Application.ActiveScene.remove(colliding_game_object)

        # Player and power up collide
        if isinstance(colliding_game_object, PowerUp):
            if colliding_game_object.power_up_type == PowerUpType.Heal:
                handle_power_up_collision(colliding_game_object, 5, 15, "Press E to heal")
                handle_power_up_selected(self.parent, colliding_game_object, PowerUpType.Heal)
            elif colliding_game_object.power_up_type == PowerUpType.Attack:
                handle_power_up_collision(colliding_game_object, 1, 5, "Press E to increase attack damage")
                handle_power_up_selected(self.parent, colliding_game_object, PowerUpType.Attack)
            elif colliding_game_object.power_up_type == PowerUpType.Defense:
                handle_power_up_collision(colliding_game_object, 1, 5, "Press E to increase defense")
                handle_power_up_selected(self.parent, colliding_game_object, PowerUpType.Defense)
            elif colliding_game_object.power_up_type == PowerUpType.Speed:
                handle_power_up_collision(colliding_game_object, 1, 5, "Press E to increase speed")
                handle_power_up_selected(self.parent, colliding_game_object, PowerUpType.Speed)
            else:
                Constants.EVENT_DISPATCHER.dispatch_event(
                    EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                              ["Press E to get a random power up"]))
                random_type = random.choice([PowerUpType.Heal, PowerUpType.Speed, PowerUpType.Attack,
                                             PowerUpType.Defense])
                if random_type == PowerUpType.Heal:
                    colliding_game_object.power_up_value = min(random.randint(-8, 10), random.randint(-8, 10))
                else:
                    colliding_game_object.power_up_value = min(random.randint(-3, 3), random.randint(-3, 3))

                handle_power_up_selected(self.parent, colliding_game_object, random_type)

        # Player and pet collide
        if colliding_game_object.game_object_category == GameObjectCategory.Pet:
            Constants.EVENT_DISPATCHER.dispatch_event(
                EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                          ["You found a stranded dog! Press E to adopt"]))
            if Constants.INPUT_HANDLER.is_tap(pygame.K_e, 100):
                colliding_game_object.get_component(PetController).adopt()
                Constants.EVENT_DISPATCHER.dispatch_event(
                    EventData(EventCategoryType.CollisionManager, EventActionType.RemoveCollliderFromQuadTree,
                              [colliding_game_object.get_component(BoxCollider2D)]))
                colliding_game_object.remove_component(BoxCollider2D)
