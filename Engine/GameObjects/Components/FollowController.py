from abc import ABC, abstractmethod

from Engine.GameObjects.Components.Component import Component


class FollowController(Component, ABC):
    def __init__(self, name, target):
        super().__init__(name)
        self._target = target

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        self._target = target

    @abstractmethod
    def _follow_target(self):
        pass