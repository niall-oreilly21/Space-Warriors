import pygame

from Engine.Graphics.Sprites.Take import Take
from Engine.Other.Enums.ActiveTake import ActiveTake


class Constants:
    CHARACTER_MOVE_SPEED = 6

    class Player:
        PLAYER_MOVE_X_FRAME_RECTS = [
            pygame.Rect(83, 718, 45, 48), pygame.Rect(147, 717, 45, 48), pygame.Rect(211, 717, 44, 48),
            pygame.Rect(274, 716, 40, 50), pygame.Rect(337, 717, 34, 49), pygame.Rect(402, 717, 40, 49),
            pygame.Rect(467, 717, 45, 49), pygame.Rect(531, 717, 45, 49)
        ]
        PLAYER_MOVE_X = Take(ActiveTake.PLAYER_MOVE_X, PLAYER_MOVE_X_FRAME_RECTS)

        PLAYER_MOVE_DOWN_FRAME_RECTS = [
            pygame.Rect(82, 653, 28, 49), pygame.Rect(147, 653, 27, 50), pygame.Rect(211, 654, 27, 50),
            pygame.Rect(274, 653, 28, 50), pygame.Rect(338, 653, 28, 49), pygame.Rect(402, 653, 27, 50),
            pygame.Rect(467, 654, 26, 49), pygame.Rect(530, 653, 28, 50)
        ]
        PLAYER_MOVE_DOWN = Take(ActiveTake.PLAYER_MOVE_DOWN, PLAYER_MOVE_DOWN_FRAME_RECTS)

        PLAYER_MOVE_UP_FRAME_RECTS = [
            pygame.Rect(81, 523, 29, 51), pygame.Rect(145, 521, 29, 54), pygame.Rect(209, 526, 29, 50),
            pygame.Rect(273, 521, 29, 54), pygame.Rect(337, 524, 29, 50), pygame.Rect(401, 524, 29, 51),
            pygame.Rect(465, 525, 29, 51), pygame.Rect(529, 523, 29, 52)
        ]
        PLAYER_MOVE_UP = Take(ActiveTake.PLAYER_MOVE_UP, PLAYER_MOVE_UP_FRAME_RECTS)

        PLAYER_ANIMATOR_INFO = [PLAYER_MOVE_X, PLAYER_MOVE_DOWN, PLAYER_MOVE_UP]

    class EnemyWolf:
        ENEMY_MOVE_X_FRAME_RECTS = [
            pygame.Rect(84, 723, 27, 43), pygame.Rect(149, 722, 26, 43), pygame.Rect(211, 722, 28, 43),
            pygame.Rect(274, 722, 29, 44), pygame.Rect(336, 723, 31, 43), pygame.Rect(402, 722, 29, 44),
            pygame.Rect(467, 722, 28, 44), pygame.Rect(532, 722, 27, 44)
        ]
        ENEMY_MOVE_X = Take(ActiveTake.ENEMY_WOLF_MOVE_X, ENEMY_MOVE_X_FRAME_RECTS)

        ENEMY_MOVE_DOWN_FRAME_RECTS = [
            pygame.Rect(81, 659, 30, 43), pygame.Rect(145, 659, 30, 44), pygame.Rect(210, 660, 29, 43),
            pygame.Rect(273, 659, 30, 44), pygame.Rect(337, 659, 30, 43), pygame.Rect(401, 659, 30, 44),
            pygame.Rect(465, 660, 29, 43), pygame.Rect(529, 659, 30, 44)
        ]
        ENEMY_MOVE_DOWN = Take(ActiveTake.ENEMY_WOLF_MOVE_DOWN, ENEMY_MOVE_DOWN_FRAME_RECTS)

        ENEMY_MOVE_UP_FRAME_RECTS = [
            pygame.Rect(81, 531, 30, 42), pygame.Rect(145, 531, 30, 43), pygame.Rect(209, 532, 29, 43),
            pygame.Rect(273, 531, 30, 43), pygame.Rect(337, 531, 30, 42), pygame.Rect(401, 531, 30, 43),
            pygame.Rect(466, 532, 29, 43), pygame.Rect(529, 531, 30, 43)
        ]
        ENEMY_MOVE_UP = Take(ActiveTake.ENEMY_WOLF_MOVE_UP, ENEMY_MOVE_UP_FRAME_RECTS)

        ENEMY_ANIMATOR_INFO = [ENEMY_MOVE_X, ENEMY_MOVE_DOWN, ENEMY_MOVE_UP]

    class EnemyRat:
        MOVE_X_Y = 715
        MOVE_X_HEIGHT = 51

        ENEMY_MOVE_X_FRAME_RECTS = [
            pygame.Rect(84, MOVE_X_Y, 44, MOVE_X_HEIGHT), pygame.Rect(149, MOVE_X_Y, 43, MOVE_X_HEIGHT),
            pygame.Rect(211, MOVE_X_Y, 44, MOVE_X_HEIGHT), pygame.Rect(274, MOVE_X_Y, 40, MOVE_X_HEIGHT),
            pygame.Rect(336, MOVE_X_Y, 34, MOVE_X_HEIGHT), pygame.Rect(402, MOVE_X_Y, 38, MOVE_X_HEIGHT),
            pygame.Rect(467, MOVE_X_Y, 43, MOVE_X_HEIGHT), pygame.Rect(532, MOVE_X_Y, 44, MOVE_X_HEIGHT)
        ]
        ENEMY_MOVE_X = Take(ActiveTake.ENEMY_RAT_MOVE_X, ENEMY_MOVE_X_FRAME_RECTS)

        ENEMY_MOVE_DOWN_FRAME_RECTS = [
            pygame.Rect(81, 658, 30, 44), pygame.Rect(145, 658, 30, 45), pygame.Rect(210, 659, 30, 45),
            pygame.Rect(273, 658, 30, 45), pygame.Rect(337, 658, 30, 44), pygame.Rect(401, 658, 30, 45),
            pygame.Rect(465, 659, 29, 44), pygame.Rect(529, 658, 30, 45)
        ]
        ENEMY_MOVE_DOWN = Take(ActiveTake.ENEMY_RAT_MOVE_DOWN, ENEMY_MOVE_DOWN_FRAME_RECTS)

        ENEMY_MOVE_UP_FRAME_RECTS = [
            pygame.Rect(81, 523, 35, 50), pygame.Rect(145, 521, 36, 53), pygame.Rect(209, 527, 32, 48),
            pygame.Rect(273, 521, 36, 53), pygame.Rect(337, 524, 36, 49), pygame.Rect(401, 524, 36, 50),
            pygame.Rect(466, 525, 35, 50), pygame.Rect(529, 523, 36, 51)
        ]
        ENEMY_MOVE_UP = Take(ActiveTake.ENEMY_RAT_MOVE_UP, ENEMY_MOVE_UP_FRAME_RECTS)

        ENEMY_ANIMATOR_INFO = [ENEMY_MOVE_X, ENEMY_MOVE_DOWN, ENEMY_MOVE_UP]

    class EnemyAlien:
        ENEMY_MOVE_X_FRAME_RECTS = [
            pygame.Rect(84, 721, 35, 45), pygame.Rect(149, 720, 36, 45), pygame.Rect(211, 720, 36, 45),
            pygame.Rect(274, 720, 36, 46), pygame.Rect(336, 721, 33, 45), pygame.Rect(402, 720, 36, 46),
            pygame.Rect(467, 720, 36, 46), pygame.Rect(532, 720, 37, 46)
        ]
        ENEMY_MOVE_X = Take(ActiveTake.ENEMY_ALIEN_MOVE_X, ENEMY_MOVE_X_FRAME_RECTS)

        ENEMY_MOVE_DOWN_FRAME_RECTS = [
            pygame.Rect(81, 657, 32, 45), pygame.Rect(145, 657, 30, 46), pygame.Rect(210, 658, 30, 46),
            pygame.Rect(273, 657, 30, 46), pygame.Rect(337, 657, 32, 45), pygame.Rect(401, 657, 31, 46),
            pygame.Rect(465, 658, 30, 45), pygame.Rect(529, 657, 31, 46)
        ]
        ENEMY_MOVE_DOWN = Take(ActiveTake.ENEMY_ALIEN_MOVE_DOWN, ENEMY_MOVE_DOWN_FRAME_RECTS)

        ENEMY_MOVE_UP_FRAME_RECTS = [
            pygame.Rect(81, 524, 30, 49), pygame.Rect(145, 523, 30, 51), pygame.Rect(209, 528, 29, 47),
            pygame.Rect(273, 523, 30, 51), pygame.Rect(337, 524, 30, 49), pygame.Rect(401, 524, 30, 50),
            pygame.Rect(466, 526, 29, 49), pygame.Rect(529, 524, 30, 50)
        ]
        ENEMY_MOVE_UP = Take(ActiveTake.ENEMY_ALIEN_MOVE_UP, ENEMY_MOVE_UP_FRAME_RECTS)

        ENEMY_ANIMATOR_INFO = [ENEMY_MOVE_X, ENEMY_MOVE_DOWN, ENEMY_MOVE_UP]

    class PetDog:
        PET_WALK_FRAME_RECTS = [
            pygame.Rect(110, 276, 37, 28), pygame.Rect(174, 275, 34, 28), pygame.Rect(238, 276, 34, 28),
            pygame.Rect(304, 277, 32, 27), pygame.Rect(368, 275, 32, 29),
        ]
        PET_WALK = Take(ActiveTake.PET_DOG_WALK, PET_WALK_FRAME_RECTS)

        PET_ANIMATOR_INFO = [PET_WALK]
