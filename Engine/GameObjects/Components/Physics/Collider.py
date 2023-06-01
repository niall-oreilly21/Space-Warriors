from abc import abstractmethod, ABC
from enum import Enum


from Engine.GameObjects.Components.Component import Component
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D


class Collider(Component, ABC):

    def __init__(self, name):
        super().__init__(name)

    @abstractmethod
    def handle_response(self, colliding_game_object):
        pass
    def clone(self):
        pass

