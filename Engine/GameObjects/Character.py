from abc import ABC

from enum import Enum

from Engine.GameObjects.GameObject import GameObject
from Engine.Other.Enums.GameObjectEnums import GameObjectType, GameObjectCategory
from Engine.Other.Interfaces.ICloneable import ICloneable
from Engine.Other.Interfaces.IDamageable import IDamageable
from Engine.Other.Transform2D import Transform2D


class Character(GameObject, IDamageable, ICloneable):
    def __init__(self, name, health, attack_damage, damage_cooldown, initial_position, transform=None,
                 game_object_type=GameObjectType.Dynamic, game_object_category=GameObjectCategory.Entity):
        super().__init__(name, transform, game_object_type, game_object_category)
        self.__health = health
        self.__attack_damage = attack_damage
        self.__is_damaged = False
        self.__damage_cooldown = damage_cooldown
        self.__health_bar = None
        self.__last_damage_time = 0
        self.__initial_position = initial_position
        self.__initial_health = health

    @property
    def health(self):
        return self.__health

    def is_hit(self):
        return self.__health < self.__initial_health

    @property
    def initial_health(self):
        return self.__initial_health

    @initial_health.setter
    def initial_health(self, initial_health):
        self.__initial_health = initial_health

    def reset_health(self):
        self.__health = self.__initial_health

    def reset_position(self):
        self.transform.position = self.__initial_position

    @health.setter
    def health(self, health):
        self.__health = health

    def damage(self, damage):
        self.__health -= damage

    @property
    def attack_damage(self):
        return self.__attack_damage

    @attack_damage.setter
    def attack_damage(self, damage):
        self.__attack_damage = damage

    @property
    def is_damaged(self):
        return self.__is_damaged

    @is_damaged.setter
    def is_damaged(self, is_damaged):
        self.__is_damaged = is_damaged

    @property
    def last_damage_time(self):
        return self.__last_damage_time

    @last_damage_time.setter
    def last_damage_time(self, last_damage_time):
        self.__last_damage_time = last_damage_time

    @property
    def damage_cooldown(self):
        return self.__damage_cooldown

    @damage_cooldown.setter
    def damage_cooldown(self, cooldown):
        self.__damage_cooldown = cooldown

    @property
    def initial_position(self):
        return self.__initial_position

    @initial_position.setter
    def initial_position(self, position):
        self.__initial_position = position

    @property
    def health_bar(self):
        return self.__health_bar

    @health_bar.setter
    def health_bar(self, health_bar):
        self.__health_bar = health_bar

    def clone(self):
        character = Character(self.name, self.health, self.attack_damage, self.damage_cooldown, self.initial_position.copy(), self.transform.clone(), self.game_object_type, self.game_object_category)

        for component in self._components:
            cloned_component = component.clone()
            character.add_component(cloned_component)

        return character
