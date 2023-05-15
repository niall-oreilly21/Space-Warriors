from abc import ABC, abstractmethod

class MovementInterface(ABC):
    @abstractmethod
    def _move_left(self, game_time):
        pass

    @abstractmethod
    def _move_right(self, game_time):
        pass

    @abstractmethod
    def _move_up(self, game_time):
        pass

    @abstractmethod
    def _move_down(self, game_time):
        pass
