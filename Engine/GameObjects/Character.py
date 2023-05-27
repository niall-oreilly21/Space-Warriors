from abc import ABC

from enum import Enum

from Engine.GameObjects.GameObject import GameObject
from Engine.Other.Enums.GameObjectEnums import GameObjectType, GameObjectCategory
from Engine.Other.Interfaces.ICloneable import ICloneable
from Engine.Other.Interfaces.IDamageable import IDamageable
from Engine.Other.Transform2D import Transform2D


class Character(GameObject, IDamageable, ICloneable):
    def __init__(self, name, health, transform=None, game_object_type=GameObjectType.Static, game_object_category=GameObjectCategory.Entity):
        super().__init__(name, transform, game_object_type, game_object_category)
        self.__health = health

    @property
    def health(self):
        return self.__health

    def damage(self, damage):
        self.__health -= damage
        pass

    def clone(self):
        pass