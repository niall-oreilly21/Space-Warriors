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
    PET_DOG_WALK = 14,
    PLAYER_IDLE_X = 15,
    PLAYER_IDLE_UP = 16,
    PLAYER_IDLE_DOWN = 17,
    PLAYER_ATTACK_X = 18,
    PLAYER_ATTACK_DOWN = 19,
    PLAYER_ATTACK_UP = 20,
    COOK = 21,
    TELEPORT = 22,
    PET_DOG_SIT = 23,
    PET_DOG_RUN = 24,
    PET_DOG_IDLE = 25
    TELEPORT_IDLE = 26
