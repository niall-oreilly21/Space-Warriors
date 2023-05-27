from enum import Enum


class GameObjectType(Enum):
    Static = 0
    Dynamic = 1


class GameObjectCategory(Enum):
    Player = 0


class GameObjectDirection(Enum):
    Up = 0
    Down = 1
    Left = 2
    Right = 3


class GameObjectEnemyType(Enum):
    Wolf = 0
    Rat = 1
    Alien = 2
