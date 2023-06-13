import random

from App.Constants.Application import Application
from Engine.GameObjects.Components.Component import Component
from Engine.GameObjects.Components.FollowController import FollowController
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.GameObjects.GameObject import GameObject
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Other.Enums.GameObjectEnums import GameObjectType, GameObjectCategory


class Gun(GameObject):
    def __init__(self, name, bullet_prefab, fire_rate_per_sec, colors, transform=None, game_object_type=GameObjectType.Dynamic, game_object_category=GameObjectCategory.Gun):
        super().__init__(name, transform, game_object_type, game_object_category)
        self.__bullet_prefab = bullet_prefab
        self.__intial_fire_rate_per_sec = fire_rate_per_sec
        self.__fire_rate_per_sec = self.__intial_fire_rate_per_sec  * 1000
        self.__can_fire = True
        self.__colors = colors
        self.__elapsed_time = 0


    def update(self, game_time):
        super().update(game_time)

        self.__elapsed_time += game_time.elapsed_time

        if self.__elapsed_time >= self.__fire_rate_per_sec:
            self.__can_fire = True
            self.__elapsed_time = 0

    def fire(self, direction):
        if self.__can_fire:
            bullet = self.__create_bullet()
            bullet.fire(direction, random.choice(self.__colors))
            self.__can_fire = False


    def __create_bullet(self):
        bullet = self.__bullet_prefab.clone()
        bullet.transform.position = self.transform.position
        return bullet

    def clone(self):
        gun = Gun(self.name, self.__bullet_prefab.clone(), self.__intial_fire_rate_per_sec, self.__colors, self.transform.clone(), self.game_object_type, self.game_object_category)

        for component in self._components:
            cloned_component = component.clone()
            gun.add_component(cloned_component)

        return gun





