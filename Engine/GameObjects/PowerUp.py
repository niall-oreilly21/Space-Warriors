import random

from Engine.GameObjects.GameObject import GameObject
from Engine.Other.Enums.GameObjectEnums import GameObjectType, GameObjectCategory, PowerUpType


class PowerUp(GameObject):
    def __init__(self, name, power_up_type,  transform=None, game_object_type=GameObjectType.Static,
                 game_object_category=GameObjectCategory.PowerUp):
        super().__init__(name, transform, game_object_type, game_object_category)
        self.__power_up_type = power_up_type
        self.__power_up_value = 0

    @property
    def power_up_type(self):
        return self.__power_up_type

    @property
    def power_up_value(self):
        return self.__power_up_value

    @power_up_value.setter
    def power_up_value(self, val):
        self.__power_up_value = val

    def clone(self):
        power_up = PowerUp(self.name, self.power_up_type, self.transform.clone(), self.game_object_type, self.game_object_category)

        for component in self._components:
            cloned_component = component.clone()
            power_up.add_component(cloned_component)

        return power_up

