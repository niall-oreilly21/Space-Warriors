from abc import ABC

from enum import Enum

from Engine.Other.Transform2D import Transform2D


class GameObjectType(Enum):
    Static = 0
    Dynamic = 1

class GameObjectCategory(Enum):
    Player = 0


class GameObject(ABC):
    def __init__(self, name, transform = None, type=GameObjectType.Static, category=GameObjectCategory.Player):
        self.name = name
        self.transform = transform
        self.components = []
        self.type = type
        self.category = category

        if self.transform is None:
            self.transform = Transform2D()

    def add_component(self, component):
        if component.transform == None:
            component.transform = self.transform

        if component.parent == None:
            component.parent = self

        self.components.append(component)

    def remove_component(self, component):
        if component in self.components:
            self.components.remove(component)

    def get_component(self, component_type):
        for component in self.components:
            if isinstance(component, component_type):
                return component
        return None

    def update(self, game_time):
        for  component in self.components:
            component.update(game_time)










