from abc import ABC, abstractmethod


class IUpdateable(ABC):

    @abstractmethod
    def update(self, game_time):
        pass

