from enum import Enum


class GameObjectType(Enum):
    Static = 0
    Dynamic = 1

class GameObjectCategory(Enum):
    Entity = 0
    Player = 1