from abc import abstractmethod, ABC


class IDamageable(ABC):
    @abstractmethod
    def damage(self, damage):
        pass