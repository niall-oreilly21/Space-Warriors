from abc import ABC, abstractmethod

class Component(ABC):
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.transform = None

    def update(self, game_time):
        pass
