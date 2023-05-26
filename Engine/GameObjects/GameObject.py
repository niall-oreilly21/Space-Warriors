from abc import ABC

from enum import Enum

from Engine.Other.Enums.GameObjectEnums import GameObjectType, GameObjectCategory
from Engine.Other.Transform2D import Transform2D

class GameObject():
    def __init__(self, name, transform = None, type=GameObjectType.Static, category=GameObjectCategory.Player):
        self.__name = name
        self.__transform = transform
        self.__components = []
        self.__type = type
        self.__category = category

        if self.__transform is None:
            self.__transform = Transform2D

    @property
    def name(self):
        return self.__name

    @property
    def transform(self):
        return self.__transform

    @property
    def type(self):
        return self.__type

    @property
    def category(self):
        return self.__category

    def get_components(self, component_type):
        components = []
        for component in self.__components:
            if isinstance(component, component_type):
                components.append(component)
        return components

    def add_component(self, component):
        if component.transform == None:
            component.transform = self.__transform

        if component.parent == None:
            component.parent = self

        self.__components.append(component)

    def remove_component(self, component):
        if component in self.__components:
            self.__components.remove(component)

    def get_component(self, component_type):
        for component in self.__components:
            if isinstance(component, component_type):
                return component
        return None

    def update(self, game_time):
        for  component in self.__components:
            component.update(game_time)

    def start(self):
        for  component in self.__components:
            component.start()








