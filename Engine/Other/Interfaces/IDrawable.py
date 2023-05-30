from abc import abstractmethod, ABC


class IDrawable(ABC):
    @abstractmethod
    def draw(self):
        pass