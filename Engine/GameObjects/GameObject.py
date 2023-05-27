from abc import ABC

from enum import Enum

from pygame import Vector2

from Engine.Other.Enums.GameObjectEnums import GameObjectType, GameObjectCategory
from Engine.Other.Interfaces.ICloneable import ICloneable
from Engine.Other.Transform2D import Transform2D

class GameObject(ICloneable):
    def __init__(self, name, transform = None, game_object_type=GameObjectType.Static, game_object_category=GameObjectCategory.Entity):
        self.__name = name
        self.__transform = transform
        self._components = []
        self.__game_object_type = game_object_type
        self.__game_object_category = game_object_category

        if self.__transform is None:
            self.__transform = Transform2D(Vector2(0, 0), 0, Vector2(1, 1))

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def transform(self):
        return self.__transform

    @property
    def game_object_type(self):
        return self.__game_object_type

    @property
    def game_object_category(self):
        return self.__game_object_category

    def get_components(self, component_type):
        components = []
        for component in self._components:
            if isinstance(component, component_type):
                components.append(component)
        return components

    def add_component(self, component):
        component.transform = self.__transform
        component.parent = self
        self._components.append(component)

    def remove_component(self, component_type):
        for component in self._components:
            if isinstance(component, component_type):
                self._components.remove(component)

    def get_component(self, component_type):
        for component in self._components:
            if isinstance(component, component_type):
                return component
        return None

    def update(self, game_time):
        for  component in self._components:
            component.update(game_time)

    def start(self):
        for  component in self._components:
            component.start()

    def clone(self):
        clone_game_object = GameObject(self.__name, self.__transform.clone(), self.__game_object_type, self.__game_object_category)

        for component in self._components:
            cloned_component = component.clone()
            clone_game_object.add_component(cloned_component)

        return clone_game_object








