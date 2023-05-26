from abc import ABC, abstractmethod


class IStartable(ABC):
    @abstractmethod
    def update(self):
        pass