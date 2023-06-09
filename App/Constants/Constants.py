import pygame
from pygame import Vector2

from Engine.Graphics.Materials.TextureMaterial2D import TextureMaterial2D
from Engine.Graphics.Sprites.Take import Take
from Engine.Managers.EventSystem.EventDispatcher import EventDispatcher
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.InputHandler import InputHandler


class Constants:
    GAME_NAME = "Space Warriors"

    EVENT_DISPATCHER = EventDispatcher()
    INPUT_HANDLER = None

    VIEWPORT_WIDTH = 1500
    VIEWPORT_HEIGHT = 750

    CHARACTER_ANIMATOR_MOVE_SPEED = 5

    class Player:
        WIDTH = 29

        DEFAULT_HEALTH = 200
        DEFAULT_ATTACK_DAMAGE = 5

        MOVE_SPEED = 0.2
        DAMAGE_COOLDOWN = 1

        __MOVE_X_Y = 712
        __MOVE_X_HEIGHT = 54

        __PLAYER_MOVE_X_FRAME_RECTS = [
            pygame.Rect(83, __MOVE_X_Y, 45, __MOVE_X_HEIGHT), pygame.Rect(147, __MOVE_X_Y, 45, __MOVE_X_HEIGHT),
            pygame.Rect(211, __MOVE_X_Y, 44, __MOVE_X_HEIGHT), pygame.Rect(274, __MOVE_X_Y, 40, __MOVE_X_HEIGHT),
            pygame.Rect(337, __MOVE_X_Y, 34, __MOVE_X_HEIGHT), pygame.Rect(402, __MOVE_X_Y, 40, __MOVE_X_HEIGHT),
            pygame.Rect(467, __MOVE_X_Y, 45, __MOVE_X_HEIGHT), pygame.Rect(531, __MOVE_X_Y, 45, __MOVE_X_HEIGHT)
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

        __PLAYER_IDLE_X_FRAME_RECT = [pygame.Rect(19, 712, 38, 54)]
        __PLAYER_IDLE_X = Take(ActiveTake.PLAYER_IDLE_X, __PLAYER_IDLE_X_FRAME_RECT)

        __PLAYER_IDLE_DOWN_FRAME_RECT = [pygame.Rect(9, 653, 37, 51)]
        __PLAYER_IDLE_DOWN = Take(ActiveTake.PLAYER_IDLE_DOWN, __PLAYER_IDLE_DOWN_FRAME_RECT)

        __PLAYER_IDLE_UP_FRAME_RECT = [pygame.Rect(8, 525, 39, 48)]
        __PLAYER_IDLE_UP = Take(ActiveTake.PLAYER_IDLE_UP, __PLAYER_IDLE_UP_FRAME_RECT)

        __PLAYER_ATTACK_X_FRAME_RECT = [pygame.Rect(83, 1997, 93, 51), pygame.Rect(277, 1999, 93, 51),
                                        pygame.Rect(458, 1997, 93, 51), pygame.Rect(641, 1997, 93, 51),
                                        pygame.Rect(852, 1997, 93, 51), pygame.Rect(1044, 1997, 93, 51)]

        __PLAYER_ATTACK_X = Take(ActiveTake.PLAYER_ATTACK_X, __PLAYER_ATTACK_X_FRAME_RECT, False, 1)

        __PLAYER_ATTACK_UP_FRAME_RECT = [pygame.Rect(72, 1404, 38, 67), pygame.Rect(255, 1404, 46, 67),
                                         pygame.Rect(448, 1404, 44, 67), pygame.Rect(629, 1404, 57, 67),
                                         pygame.Rect(821, 1404, 81, 67), pygame.Rect(1043, 1404, 76, 67)]

        __PLAYER_ATTACK_UP = Take(ActiveTake.PLAYER_ATTACK_UP, __PLAYER_ATTACK_UP_FRAME_RECT, False, 1)

        __PLAYER_ATTACK_DOWN_FRAME_RECT = [pygame.Rect(72, 1805, 38, 52), pygame.Rect(255, 1805, 46, 49),
                                           pygame.Rect(448, 1807, 44, 47), pygame.Rect(632, 1806, 55, 48),
                                           pygame.Rect(821, 1805, 81, 68), pygame.Rect(1044, 1805, 75, 65)]

        __PLAYER_ATTACK_DOWN = Take(ActiveTake.PLAYER_ATTACK_DOWN, __PLAYER_ATTACK_DOWN_FRAME_RECT, False, 1)

        PLAYER_ANIMATOR_INFO = [__PLAYER_MOVE_X, __PLAYER_MOVE_DOWN, __PLAYER_MOVE_UP, __PLAYER_IDLE_X,
                                __PLAYER_IDLE_DOWN, __PLAYER_IDLE_UP, __PLAYER_ATTACK_X, __PLAYER_ATTACK_UP,
                                __PLAYER_ATTACK_DOWN]

        __GIRL_SPRITE_SHEET = pygame.image.load("Assets/SpriteSheets/Characters/player_girl.png")
        __BOY_SPRITE_SHEET = pygame.image.load("Assets/SpriteSheets/Characters/player_boy.png")

        MATERIAL_GIRL = TextureMaterial2D(__GIRL_SPRITE_SHEET, None, Vector2(0, 0), None)
        MATERIAL_BOY = TextureMaterial2D(__BOY_SPRITE_SHEET, None,  Vector2(0, 0), None)

    class EnemyWolf:
        MOVE_SPEED = 3

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

        MATERIAL_ENEMY1 = TextureMaterial2D(__ENEMY_SPRITE_SHEET_1, None, Vector2(0, 0), None)
        MATERIAL_ENEMY2 = TextureMaterial2D(__ENEMY_SPRITE_SHEET_2, None, Vector2(0, 0), None)
        MATERIAL_ENEMY3 = TextureMaterial2D(__ENEMY_SPRITE_SHEET_3, None, Vector2(0, 0), None)

    class EnemyRat:
        MOVE_SPEED = 3

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

        MATERIAL_ENEMY1 = TextureMaterial2D(__ENEMY_SPRITE_SHEET_1, None, Vector2(0, 0), None)
        MATERIAL_ENEMY2 = TextureMaterial2D(__ENEMY_SPRITE_SHEET_2, None, Vector2(0, 0), None)
        MATERIAL_ENEMY3 = TextureMaterial2D(__ENEMY_SPRITE_SHEET_3, None,  Vector2(0, 0), None)

    class EnemyAlien:
        MOVE_SPEED = 1.5

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

        MATERIAL_ENEMY1 = TextureMaterial2D(__ENEMY_SPRITE_SHEET_1, None, Vector2(0, 0), None)
        MATERIAL_ENEMY2 = TextureMaterial2D(__ENEMY_SPRITE_SHEET_2, None, Vector2(0, 0), None)
        MATERIAL_ENEMY3 = TextureMaterial2D(__ENEMY_SPRITE_SHEET_3, None, Vector2(0, 0), None)

    class PetDog:
        __PET_WALK_FRAME_RECTS = [
            pygame.Rect(110, 276, 37, 28), pygame.Rect(174, 275, 34, 28), pygame.Rect(238, 276, 34, 28),
            pygame.Rect(304, 277, 32, 27), pygame.Rect(368, 275, 32, 29),
        ]
        __PET_WALK = Take(ActiveTake.PET_DOG_WALK, __PET_WALK_FRAME_RECTS)

        __PET_RUN_FRAME_RECTS = [
            pygame.Rect(111, 343, 37, 23), pygame.Rect(175, 343, 36, 25), pygame.Rect(240, 342, 35, 26),
            pygame.Rect(305, 340, 34, 28), pygame.Rect(373, 339, 32, 28), pygame.Rect(438, 339, 32, 29),
            pygame.Rect(503, 339, 32, 29), pygame.Rect(565, 342, 36, 26),
        ]
        __PET_RUN = Take(ActiveTake.PET_DOG_RUN, __PET_RUN_FRAME_RECTS)

        __PET_SIT_FRAME_RECT = [
            pygame.Rect(304, 211, 30, 29), pygame.Rect(368, 211, 30, 29), pygame.Rect(432, 211, 30, 29),
            pygame.Rect(496, 211, 30, 29), pygame.Rect(560, 211, 30, 29), pygame.Rect(624, 211, 30, 29)
        ]
        __PET_SIT = Take(ActiveTake.PET_DOG_SIT, __PET_SIT_FRAME_RECT)

        __PET_IDLE_FRAME_RECT = [
            pygame.Rect(112, 84, 32, 28), pygame.Rect(176, 83, 32, 29), pygame.Rect(240, 84, 32, 28),
            pygame.Rect(304, 83, 32, 29), pygame.Rect(368, 85, 32, 27)
        ]
        __PET_IDLE = Take(ActiveTake.PET_DOG_IDLE, __PET_IDLE_FRAME_RECT)

        PET_ANIMATOR_INFO = [__PET_WALK, __PET_SIT, __PET_RUN]

        __PET_SPRITE_SHEET = pygame.image.load("Assets/SpriteSheets/Characters/pet_dog.png")

        MATERIAL_PET = TextureMaterial2D(__PET_SPRITE_SHEET, None, Vector2(0, 0), None)

    class Menu:
        __MAIN_MENU_BACKGROUND = pygame.image.load("Assets/UI/Menu/main_menu.png")
        MATERIAL_MAIN_MENU = TextureMaterial2D(__MAIN_MENU_BACKGROUND, None, Vector2(0, 0), None)

        __PAUSE_MENU_BACKGROUND = pygame.image.load("Assets/UI/Menu/pause_menu.png")
        MATERIAL_PAUSE_MENU = TextureMaterial2D(__PAUSE_MENU_BACKGROUND, None, Vector2(0, 0), None)

        __SOUND_MENU_BACKGROUND = __PAUSE_MENU_BACKGROUND
        MATERIAL_SOUND_MENU = TextureMaterial2D(__SOUND_MENU_BACKGROUND, None, Vector2(0, 0), None)

        __DEATH_MENU_BACKGROUND = __PAUSE_MENU_BACKGROUND
        MATERIAL_DEATH_MENU = TextureMaterial2D(__DEATH_MENU_BACKGROUND, None, Vector2(0, 0), None)

        __STARS_FRAME_RECT = [pygame.Rect(252, 14, 91, 119), pygame.Rect(154, 14, 91, 119), pygame.Rect(14, 14, 91, 119),
                              pygame.Rect(154, 14, 91, 119), pygame.Rect(252, 14, 91, 119)]
        __STARS = Take(ActiveTake.STAR, __STARS_FRAME_RECT)
        STARS_ANIMATOR_INFO = [__STARS]

        __STARS_SPRITE_SHEET = pygame.image.load("Assets/UI/stars.png")
        MATERIAL_STARS = TextureMaterial2D(__STARS_SPRITE_SHEET, None, Vector2(0, 0), None)

        TITLE_FONT_SIZE = 45
        TITLE_FONT_PATH = "Assets/Fonts/Starjedi.ttf"

        TEXT_FONT_SIZE = 40
        TEXT_FONT_PATH = "Assets/Fonts/VCR_OSD_MONO.ttf"

        MENU_BUTTON_IMAGE = pygame.image.load("Assets/UI/Menu/menu_button.png")
        BACK_BUTTON_IMAGE = pygame.image.load("Assets/UI/Menu/back_button.png")

        EARTH_IMAGE = pygame.image.load("Assets/UI/Menu/earth.png")
        MARS_IMAGE = pygame.image.load("Assets/UI/Menu/mars.png")
        SATURN_IMAGE = pygame.image.load("Assets/UI/Menu/saturn.png")

        MOVE_CONTROLS_IMAGE = pygame.image.load("Assets/UI/Menu/move_keys.png")
        ATTACK_CONTROLS_IMAGE = pygame.image.load("Assets/UI/Menu/attack_keys.png")
        ACTIVATE_CONTROL_IMAGE = pygame.image.load("Assets/UI/Menu/activate_key.png")

    class Button:
        START_BUTTON = "Start"
        QUIT_BUTTON = "Quit"
        RESUME_BUTTON = "Resume"
        MAIN_MENU_BUTTON = "Main Menu"
        EARTH_BUTTON = "Earth"
        MARS_BUTTON = "Mars"
        SATURN_BUTTON = "Saturn"
        SOUND_BUTTON = "Sound"
        MUTE_BUTTON = "Mute"
        UNMUTE_BUTTON = "Unmute"
        RESTART_BUTTON = "Restart"
        GIRL_PLAYER_BUTTON = "GirlPlayer"
        BOY_PLAYER_BUTTON = "BoyPlayer"
        CONTROLS_BUTTON = "Controls"
        BACK_BUTTON = "Back"
        LEVELS_BUTTON = "Levels"

    class Scene:
        MAIN_MENU = "MainMenuScene"
        PAUSE_MENU = "PauseMenuScene"
        DEATH_MENU = "DeathMenuScene"
        SOUND_MENU = "SoundMenuScene"
        LEVEL_MENU = "LevelMenuScene"
        EARTH = "EarthScene"
        MARS = "MarsScene"
        SATURN = "SaturnScene"
        CHARACTER_SELECTION_MENU = "CharacterSelectionMenuScene"
        CONTROLS_MENU = "ControlsMenu"

    class Camera:
        GAME_CAMERA = "GameCamera"
        MENU_CAMERA = "MenuCamera"

    class Music:
        MENU_MUSIC = "MenuMusic"
        BACKGROUND_MUSIC_EARTH = "BackgroundMusicEarth"
        BACKGROUND_MUSIC_MARS = "BackgroundMusicMars"
        BACKGROUND_MUSIC_SATURN = "BackgroundMusicSaturn"
        TELEPORT_SOUND = "TeleportSound"
        PLAYER_DEATH_SOUND = "PlayerDeathSound"
        PLAYER_ATTACK_SOUND = "PlayerAttackSound"
        BUTTON_SOUND = "ButtonSound"

    class MusicFilePath:
        MENU_MUSIC_FILEPATH = "Assets/Sounds/background_music.mp3"
        BACKGROUND_MUSIC_EARTH_FILEPATH = "Assets/Sounds/planet_a_music.mp3"
        BACKGROUND_MUSIC_MARS_FILEPATH = "Assets/Sounds/planet_b_music.wav"
        BACKGROUND_MUSIC_SATURN_FILEPATH = "Assets/Sounds/planet_c_music.mp3"
        TELEPORT_SOUND_FILEPATH = "Assets/Sounds/teleport.wav"
        PLAYER_DEATH_SOUND_FILEPATH = "Assets/Sounds/death.wav"
        PLAYER_ATTACK_SOUND_FILEPATH = "Assets/Sounds/sword_swish.wav"
        BUTTON_SOUND_FILEPATH = "Assets/Sounds/button.wav"

    class Map:
        PLANET_EARTH_JSON = "Assets/SpriteSheets/Tilesets/PlanetAv2.json"
        PLANET_MARS_JSON = "Assets/SpriteSheets/Tilesets/PlanetBAlternate.json"
        PLANET_SATURN_JSON = "Assets/SpriteSheets/Tilesets/PlanetC.json"

    class Tile:
        GRASS = 1
        WATER = 2
        DARK_GRASS = 3
        DIRT = 5
        SAND = 6
        COARSE_DIRT = 9

    class UITextPrompts:
        UI_TEXT_BOTTOM = "UITextBottom"
        UI_TEXT_RIGHT = "UITextRight"
