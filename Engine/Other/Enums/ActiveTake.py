from enum import Enum


class ActiveTake(Enum):
    PLAYER_RUNNING = 0,
    PLAYER_WALKING = 1,
    PLAYER_MOVE_X = 2,
    PLAYER_MOVE_DOWN = 3,
    PLAYER_MOVE_UP = 4,
    ENEMY_WOLF_MOVE_X = 5,
    ENEMY_WOLF_MOVE_DOWN = 6,
    ENEMY_WOLF_MOVE_UP = 7,
    ENEMY_RAT_MOVE_X = 8,
    ENEMY_RAT_MOVE_DOWN = 9,
    ENEMY_RAT_MOVE_UP = 10,
    ENEMY_ALIEN_MOVE_X = 11,
    ENEMY_ALIEN_MOVE_DOWN = 12,
    ENEMY_ALIEN_MOVE_UP = 13,
    PET_DOG_WALK = 14
