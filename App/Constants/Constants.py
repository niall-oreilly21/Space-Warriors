import pygame
from pygame import Vector2

from Engine.Graphics.Materials.TextureMaterial2D import TextureMaterial2D
from Engine.Graphics.Sprites.Take import Take
from Engine.Other.Enums.ActiveTake import ActiveTake


class Constants:
    CHARACTER_MOVE_SPEED = 6

    class Player:
        __PLAYER_MOVE_X_FRAME_RECTS = [
            pygame.Rect(83, 718, 45, 48), pygame.Rect(147, 717, 45, 48), pygame.Rect(211, 717, 44, 48),
            pygame.Rect(274, 716, 40, 50), pygame.Rect(337, 717, 34, 49), pygame.Rect(402, 717, 40, 49),
            pygame.Rect(467, 717, 45, 49), pygame.Rect(531, 717, 45, 49)
        ]
        __PLAYER_MOVE_X = Take(ActiveTake.PLAYER_MOVE_X, __PLAYER_MOVE_X_FRAME_RECTS)

        __PLAYER_MOVE_DOWN_FRAME_RECTS = [
            pygame.Rect(82, 653, 28, 49), pygame.Rect(147, 653, 27, 50), pygame.Rect(211, 654, 27, 50),
            pygame.Rect(274, 653, 28, 50), pygame.Rect(338, 653, 28, 49), pygame.Rect(402, 653, 27, 50),
            pygame.Rect(467, 654, 26, 49), pygame.Rect(530, 653, 28, 50)
        ]
        __PLAYER_MOVE_DOWN = Take(ActiveTake.PLAYER_MOVE_DOWN, __PLAYER_MOVE_DOWN_FRAME_RECTS)

        __PLAYER_MOVE_UP_FRAME_RECTS = [
            pygame.Rect(81, 523, 29, 51), pygame.Rect(145, 521, 29, 54), pygame.Rect(209, 526, 29, 50),
            pygame.Rect(273, 521, 29, 54), pygame.Rect(337, 524, 29, 50), pygame.Rect(401, 524, 29, 51),
            pygame.Rect(465, 525, 29, 51), pygame.Rect(529, 523, 29, 52)
        ]
        __PLAYER_MOVE_UP = Take(ActiveTake.PLAYER_MOVE_UP, __PLAYER_MOVE_UP_FRAME_RECTS)

        PLAYER_ANIMATOR_INFO = [__PLAYER_MOVE_X, __PLAYER_MOVE_DOWN, __PLAYER_MOVE_UP]

        __GIRL_SPRITE_SHEET = pygame.image.load("Assets/SpriteSheets/Characters/player_girl.png")
        __BOY_SPRITE_SHEET = pygame.image.load("Assets/SpriteSheets/Characters/player_boy.png")

        MATERIAL_GIRL = TextureMaterial2D(__GIRL_SPRITE_SHEET, None, 0, Vector2(0, 0), None)
        MATERIAL_BOY = TextureMaterial2D(__BOY_SPRITE_SHEET, None, 0, Vector2(0, 0), None)

    class EnemyWolf:
        __ENEMY_MOVE_X_FRAME_RECTS = [
            pygame.Rect(84, 723, 27, 43), pygame.Rect(149, 722, 26, 43), pygame.Rect(211, 722, 28, 43),
            pygame.Rect(274, 722, 29, 44), pygame.Rect(336, 723, 31, 43), pygame.Rect(402, 722, 29, 44),
            pygame.Rect(467, 722, 28, 44), pygame.Rect(532, 722, 27, 44)
        ]
        __ENEMY_MOVE_X = Take(ActiveTake.ENEMY_WOLF_MOVE_X, __ENEMY_MOVE_X_FRAME_RECTS)

        __ENEMY_MOVE_DOWN_FRAME_RECTS = [
            pygame.Rect(81, 659, 30, 43), pygame.Rect(145, 659, 30, 44), pygame.Rect(210, 660, 29, 43),
            pygame.Rect(273, 659, 30, 44), pygame.Rect(337, 659, 30, 43), pygame.Rect(401, 659, 30, 44),
            pygame.Rect(465, 660, 29, 43), pygame.Rect(529, 659, 30, 44)
        ]
        __ENEMY_MOVE_DOWN = Take(ActiveTake.ENEMY_WOLF_MOVE_DOWN, __ENEMY_MOVE_DOWN_FRAME_RECTS)

        __ENEMY_MOVE_UP_FRAME_RECTS = [
            pygame.Rect(81, 531, 30, 42), pygame.Rect(145, 531, 30, 43), pygame.Rect(209, 532, 29, 43),
            pygame.Rect(273, 531, 30, 43), pygame.Rect(337, 531, 30, 42), pygame.Rect(401, 531, 30, 43),
            pygame.Rect(466, 532, 29, 43), pygame.Rect(529, 531, 30, 43)
        ]
        __ENEMY_MOVE_UP = Take(ActiveTake.ENEMY_WOLF_MOVE_UP, __ENEMY_MOVE_UP_FRAME_RECTS)

        ENEMY_ANIMATOR_INFO = [__ENEMY_MOVE_X, __ENEMY_MOVE_DOWN, __ENEMY_MOVE_UP]

        __ENEMY_SPRITE_SHEET_1 = pygame.image.load("Assets/SpriteSheets/Characters/enemy_wolf1.png")
        __ENEMY_SPRITE_SHEET_2 = pygame.image.load("Assets/SpriteSheets/Characters/enemy_wolf2.png")
        __ENEMY_SPRITE_SHEET_3 = pygame.image.load("Assets/SpriteSheets/Characters/enemy_wolf3.png")

        MATERIAL_ENEMY1 = TextureMaterial2D(__ENEMY_SPRITE_SHEET_1, None, 0, Vector2(0, 0), None)
        MATERIAL_ENEMY2 = TextureMaterial2D(__ENEMY_SPRITE_SHEET_2, None, 0, Vector2(0, 0), None)
        MATERIAL_ENEMY3 = TextureMaterial2D(__ENEMY_SPRITE_SHEET_3, None, 0, Vector2(0, 0), None)

    class EnemyRat:
        __MOVE_X_Y = 715
        __MOVE_X_HEIGHT = 51

        __ENEMY_MOVE_X_FRAME_RECTS = [
            pygame.Rect(84, __MOVE_X_Y, 44, __MOVE_X_HEIGHT), pygame.Rect(149, __MOVE_X_Y, 43, __MOVE_X_HEIGHT),
            pygame.Rect(211, __MOVE_X_Y, 44, __MOVE_X_HEIGHT), pygame.Rect(274, __MOVE_X_Y, 40, __MOVE_X_HEIGHT),
            pygame.Rect(336, __MOVE_X_Y, 34, __MOVE_X_HEIGHT), pygame.Rect(402, __MOVE_X_Y, 38, __MOVE_X_HEIGHT),
            pygame.Rect(467, __MOVE_X_Y, 43, __MOVE_X_HEIGHT), pygame.Rect(532, __MOVE_X_Y, 44, __MOVE_X_HEIGHT)
        ]
        __ENEMY_MOVE_X = Take(ActiveTake.ENEMY_RAT_MOVE_X, __ENEMY_MOVE_X_FRAME_RECTS)

        __ENEMY_MOVE_DOWN_FRAME_RECTS = [
            pygame.Rect(81, 658, 30, 44), pygame.Rect(145, 658, 30, 45), pygame.Rect(210, 659, 30, 45),
            pygame.Rect(273, 658, 30, 45), pygame.Rect(337, 658, 30, 44), pygame.Rect(401, 658, 30, 45),
            pygame.Rect(465, 659, 29, 44), pygame.Rect(529, 658, 30, 45)
        ]
        __ENEMY_MOVE_DOWN = Take(ActiveTake.ENEMY_RAT_MOVE_DOWN, __ENEMY_MOVE_DOWN_FRAME_RECTS)

        __ENEMY_MOVE_UP_FRAME_RECTS = [
            pygame.Rect(81, 523, 35, 50), pygame.Rect(145, 521, 36, 53), pygame.Rect(209, 527, 32, 48),
            pygame.Rect(273, 521, 36, 53), pygame.Rect(337, 524, 36, 49), pygame.Rect(401, 524, 36, 50),
            pygame.Rect(466, 525, 35, 50), pygame.Rect(529, 523, 36, 51)
        ]
        __ENEMY_MOVE_UP = Take(ActiveTake.ENEMY_RAT_MOVE_UP, __ENEMY_MOVE_UP_FRAME_RECTS)

        ENEMY_ANIMATOR_INFO = [__ENEMY_MOVE_X, __ENEMY_MOVE_DOWN, __ENEMY_MOVE_UP]

        __ENEMY_SPRITE_SHEET_1 = pygame.image.load("Assets/SpriteSheets/Characters/enemy_rat1.png")
        __ENEMY_SPRITE_SHEET_2 = pygame.image.load("Assets/SpriteSheets/Characters/enemy_rat2.png")
        __ENEMY_SPRITE_SHEET_3 = pygame.image.load("Assets/SpriteSheets/Characters/enemy_rat3.png")

        MATERIAL_ENEMY1 = TextureMaterial2D(__ENEMY_SPRITE_SHEET_1, None, 0, Vector2(0, 0), None)
        MATERIAL_ENEMY2 = TextureMaterial2D(__ENEMY_SPRITE_SHEET_2, None, 0, Vector2(0, 0), None)
        MATERIAL_ENEMY3 = TextureMaterial2D(__ENEMY_SPRITE_SHEET_3, None, 0, Vector2(0, 0), None)

    class EnemyAlien:
        __ENEMY_MOVE_X_FRAME_RECTS = [
            pygame.Rect(84, 721, 35, 45), pygame.Rect(149, 720, 36, 45), pygame.Rect(211, 720, 36, 45),
            pygame.Rect(274, 720, 36, 46), pygame.Rect(336, 721, 33, 45), pygame.Rect(402, 720, 36, 46),
            pygame.Rect(467, 720, 36, 46), pygame.Rect(532, 720, 37, 46)
        ]
        __ENEMY_MOVE_X = Take(ActiveTake.ENEMY_ALIEN_MOVE_X, __ENEMY_MOVE_X_FRAME_RECTS)

        __ENEMY_MOVE_DOWN_FRAME_RECTS = [
            pygame.Rect(81, 657, 32, 45), pygame.Rect(145, 657, 30, 46), pygame.Rect(210, 658, 30, 46),
            pygame.Rect(273, 657, 30, 46), pygame.Rect(337, 657, 32, 45), pygame.Rect(401, 657, 31, 46),
            pygame.Rect(465, 658, 30, 45), pygame.Rect(529, 657, 31, 46)
        ]
        __ENEMY_MOVE_DOWN = Take(ActiveTake.ENEMY_ALIEN_MOVE_DOWN, __ENEMY_MOVE_DOWN_FRAME_RECTS)

        __ENEMY_MOVE_UP_FRAME_RECTS = [
            pygame.Rect(81, 524, 30, 49), pygame.Rect(145, 523, 30, 51), pygame.Rect(209, 528, 29, 47),
            pygame.Rect(273, 523, 30, 51), pygame.Rect(337, 524, 30, 49), pygame.Rect(401, 524, 30, 50),
            pygame.Rect(466, 526, 29, 49), pygame.Rect(529, 524, 30, 50)
        ]
        __ENEMY_MOVE_UP = Take(ActiveTake.ENEMY_ALIEN_MOVE_UP, __ENEMY_MOVE_UP_FRAME_RECTS)

        ENEMY_ANIMATOR_INFO = [__ENEMY_MOVE_X, __ENEMY_MOVE_DOWN, __ENEMY_MOVE_UP]

        __ENEMY_SPRITE_SHEET_1 = pygame.image.load("Assets/SpriteSheets/Characters/enemy_alien1.png")
        __ENEMY_SPRITE_SHEET_2 = pygame.image.load("Assets/SpriteSheets/Characters/enemy_alien2.png")
        __ENEMY_SPRITE_SHEET_3 = pygame.image.load("Assets/SpriteSheets/Characters/enemy_alien3.png")

        MATERIAL_ENEMY1 = TextureMaterial2D(__ENEMY_SPRITE_SHEET_1, None, 0, Vector2(0, 0), None)
        MATERIAL_ENEMY2 = TextureMaterial2D(__ENEMY_SPRITE_SHEET_2, None, 0, Vector2(0, 0), None)
        MATERIAL_ENEMY3 = TextureMaterial2D(__ENEMY_SPRITE_SHEET_3, None, 0, Vector2(0, 0), None)

    class PetDog:
        __PET_WALK_FRAME_RECTS = [
            pygame.Rect(110, 276, 37, 28), pygame.Rect(174, 275, 34, 28), pygame.Rect(238, 276, 34, 28),
            pygame.Rect(304, 277, 32, 27), pygame.Rect(368, 275, 32, 29),
        ]
        __PET_WALK = Take(ActiveTake.PET_DOG_WALK, __PET_WALK_FRAME_RECTS)

        PET_ANIMATOR_INFO = [__PET_WALK]

        __PET_SPRITE_SHEET = pygame.image.load("Assets/SpriteSheets/Characters/pet_dog.png")

        MATERIAL_PET = TextureMaterial2D(__PET_SPRITE_SHEET, None, 0, Vector2(0, 0), None)