from abc import ABC

from Engine.Other.Interfaces.IStartable import IStartable
from Engine.Other.Interfaces.IUpdateable import IUpdateable


class Manager(IUpdateable, IStartable, ABC):
    def __init__(self, event_dispatcher):
        self._event_dispatcher = event_dispatcher
        self._subscribe_to_events()

    def _subscribe_to_events(self):
        pass

    def _handle_events(self, event_data):
        pass

    def update(self, game_time):
        pass
