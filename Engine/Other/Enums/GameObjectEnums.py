from enum import Enum


class GameObjectType(Enum):
    Static = 0
    Dynamic = 1


class GameObjectCategory(Enum):
    Player = 0
    Entity = 1
    Wolf = 2
    Rat = 3
    Alien = 4
    UI = 5

class GameObjectDirection(Enum):
    Up = 0
    Down = 1
    Left = 2
    Right = 3
