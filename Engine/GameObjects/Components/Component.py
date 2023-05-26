from abc import ABC


class Component(ABC):
    def __init__(self, name):
        self.__name = name
        self._parent = None
        self._transform = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

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
