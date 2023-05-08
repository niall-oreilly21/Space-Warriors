from abc import ABC, abstractmethod

class MovementInterface(ABC):
    @abstractmethod
    def move_left(self, game_time):
        pass

    @abstractmethod
    def move_right(self, game_time):
        pass

    @abstractmethod
    def move_up(self, game_time):
        pass

    @abstractmethod
    def move_down(self, game_time):
        pass
