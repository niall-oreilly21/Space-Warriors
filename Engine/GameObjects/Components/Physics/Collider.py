from abc import abstractmethod, ABC
from enum import Enum

from Engine.GameObjects.Components.Component import Component
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Other.Enums.GameObjectEnums import GameObjectCategory


class Collider(Component, ABC):

    def __init__(self, name):
        super().__init__(name)
        self.is_colliding = False

    @abstractmethod
    def handle_response(self, colliding_game_object):
        pass

    def handle_collision_exit(self):
        pass

    def _is_colliding_with_enemy(self, colliding_game_object):
        return colliding_game_object.game_object_category == GameObjectCategory.Alien or \
            colliding_game_object.game_object_category == GameObjectCategory.Wolf or \
            colliding_game_object.game_object_category == GameObjectCategory.Rat

    def clone(self):
        pass
