from abc import ABC

from Engine.Other.Interfaces.ICloneable import ICloneable


class Component( ICloneable, ABC):
    def __init__(self, name):
        self._name = name
        self._parent = None
        self._transform = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def transform(self):
        return self._transform

    @transform.setter
    def transform(self, transform):
        self._transform = transform

    def update(self, game_time):
        pass
    def start(self):
        pass

    def clone(self):
        pass
