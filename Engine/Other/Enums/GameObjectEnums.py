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
    Tile = 5
    Menu = 6
    UI = 7
    Environment = 8
    Pet = 9
    Teleporter = 10
    PowerUp = 11


class GameObjectDirection(Enum):
    Up = 0
    Down = 1
    Left = 2
    Right = 3


class PowerUpType(Enum):
    Speed = 0
    Defense = 1
    Heal = 2
    Attack = 3
    Random = 4
