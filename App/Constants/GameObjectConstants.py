from random import randint

import pygame
from pygame import Vector2

from App.Components.Colliders.PowerUpCollider import PowerUpCollider
from App.Components.Colliders.TeleporterCollider import TeleporterCollider
from App.Components.Controllers.HealthBarController import HealthBarController
from App.Constants.GameConstants import GameConstants
from App.Constants.Application import Application
from Engine.GameObjects.Components.Cameras.Camera import Camera
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.GameObject import GameObject
from Engine.GameObjects.Gun.Bullet import Bullet
from Engine.GameObjects.Gun.Gun import Gun
from Engine.GameObjects.Gun.GunController import GunController
from Engine.GameObjects.PowerUp import PowerUp
from Engine.Graphics.Materials.RectMaterial2D import RectMaterial2D
from Engine.Graphics.Materials.TextureMaterial2D import TextureMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Graphics.Sprites.Take import Take
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Enums.GameObjectEnums import GameObjectType, GameObjectCategory, PowerUpType
from Engine.Other.Transform2D import Transform2D
from Engine.Other.Enums.RendererLayers import RendererLayers

image = pygame.image.load("Assets/SpriteSheets/Tilesets/plain_tileset.png")
ruins_image = pygame.image.load("Assets/SpriteSheets/Tilesets/Assets_source.png")
rocks_image = pygame.image.load("Assets/SpriteSheets/Tilesets/Rocks_source.png")
bushes_image = pygame.image.load("Assets/SpriteSheets/Tilesets/Bushes_source.png")
image2 = pygame.image.load("Assets/SpriteSheets/Tilesets/plain_tileset2.png")
building_image = pygame.image.load("Assets/SpriteSheets/Tilesets/building_1.png")
bed_image = pygame.image.load("Assets/SpriteSheets/Tilesets/bed.png")
table_image = pygame.image.load("Assets/SpriteSheets/Tilesets/table.png")
couch_image = pygame.image.load("Assets/SpriteSheets/Tilesets/couch.png")
door_image = pygame.image.load("Assets/SpriteSheets/Tilesets/door.png")
window_image = pygame.image.load("Assets/SpriteSheets/Tilesets/window.png")


class GameObjectConstants:
    class Foliage:
        layer = RendererLayers.WorldObjects
        tree_layer = RendererLayers.AbovePlayer

        source_rect = pygame.Rect(179, 98, 27, 60)

        TALL_TREE = GameObject("Tree", Transform2D(Vector2(0, 0), 0, Vector2(3, 3)), GameObjectType.Static,
                               GameObjectCategory.Environment)
        object_frame = image.subsurface(source_rect)

        texture_surface = pygame.Surface(source_rect.size, pygame.SRCALPHA)
        texture_surface.blit(image, (0, 0), source_rect)

        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255, texture_surface)
        tree_renderer = Renderer2D("Renderer-2", texture_material, tree_layer)
        TALL_TREE.add_component(tree_renderer)

        LOW_TREE = GameObject("LowTree", Transform2D(Vector2(0, 0), 0, Vector2(3, 3)), GameObjectType.Static,
                              GameObjectCategory.Player)

        source_rect = pygame.Rect(177, 65, 30, 30)
        texture_surface = pygame.Surface(source_rect.size, pygame.SRCALPHA)
        texture_surface.blit(image, (0, 0), source_rect)

        object_frame = image.subsurface(source_rect)
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255, texture_surface)
        LOW_TREE.add_component(Renderer2D("Renderer-2", texture_material, tree_layer))

        BUSH_ONE = GameObject("BushOne", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                              GameObjectCategory.Player)
        object_frame = bushes_image.subsurface(pygame.Rect(295, 7, 36, 32))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        BUSH_ONE.add_component(Renderer2D("Renderer-2", texture_material, layer))

        BUSH_TWO = GameObject("BushTwo", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                              GameObjectCategory.Player)
        object_frame = bushes_image.subsurface(pygame.Rect(244, 6, 40, 34))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        BUSH_TWO.add_component(Renderer2D("Renderer-2", texture_material, layer))

        BUSH_THREE = GameObject("BushThree", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                                GameObjectCategory.Player)
        object_frame = bushes_image.subsurface(pygame.Rect(56, 6, 31, 29))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        BUSH_THREE.add_component(Renderer2D("Renderer-2", texture_material, layer))

        BUSH_FOUR = GameObject("BushFour", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                               GameObjectCategory.Player)
        object_frame = bushes_image.subsurface(pygame.Rect(196, 6, 39, 37))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        BUSH_FOUR.add_component(Renderer2D("Renderer-2", texture_material, layer))

        DEAD_BUSH = GameObject("BushFive", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                               GameObjectCategory.Player)
        object_frame = bushes_image.subsurface(pygame.Rect(39, 50, 20, 26))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        DEAD_BUSH.add_component(Renderer2D("Renderer-2", texture_material, layer))

        CACTUS = GameObject("Cactus", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                            GameObjectCategory.Player)
        object_frame = bushes_image.subsurface(pygame.Rect(393, 10, 31, 31))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        CACTUS.add_component(Renderer2D("Renderer-2", texture_material, layer))

        LILYPAD_ONE = GameObject("LilypadOne", Transform2D(Vector2(0, 0), 0, Vector2(2.5, 2.5)), GameObjectType.Static,
                                 GameObjectCategory.Environment)
        object_frame = image2.subsurface(pygame.Rect(173, 128, 15, 16))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        LILYPAD_ONE.add_component(Renderer2D("Renderer-2", texture_material, layer))

        LILYPAD_TWO = GameObject("LilypadTwo", Transform2D(Vector2(0, 0), 0, Vector2(2.5, 2.5)), GameObjectType.Static,
                                 GameObjectCategory.Environment)
        object_frame = image2.subsurface(pygame.Rect(156, 132, 11, 12))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        LILYPAD_TWO.add_component(Renderer2D("Renderer-2", texture_material, layer))

    class NaturalStructures:
        structures_layer = RendererLayers.BelowPlayer
        BOULDER = GameObject("Boulder", Transform2D(Vector2(0, 0), 0, Vector2(3, 3)), GameObjectType.Static,
                             GameObjectCategory.Environment)
        object_frame = image.subsurface(pygame.Rect(129, 146, 13, 12))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        BOULDER.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
        # BOULDER.add_component(BoxCollider2D("Box-3"))

        BOULDER_TWO = GameObject("BoulderTwo", Transform2D(Vector2(0, 0), 0, Vector2(3, 3)), GameObjectType.Static,
                                 GameObjectCategory.Player)
        object_frame = ruins_image.subsurface(pygame.Rect(148, 145, 40, 42))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        BOULDER_TWO.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
        # BOULDER_TWO.add_component(BoxCollider2D("Box-3"))

        ROCK_ONE = GameObject("RockOne", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                              GameObjectCategory.Player)
        object_frame = rocks_image.subsurface(pygame.Rect(193, 6, 62, 52))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        ROCK_ONE.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
        # ROCK_ONE.add_component(BoxCollider2D("Box-3"))

        # ROCK_TWO = GameObject("RockTwo", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
        #                       GameObjectCategory.Player)
        # object_frame = rocks_image.subsurface(pygame.Rect(67, 2, 58, 57))
        # texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        # ROCK_TWO.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
        # ROCK_TWO.add_component(BoxCollider2D("Box-3"))

        ROCK_THREE = GameObject("RockThree", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                                GameObjectCategory.Player)
        object_frame = rocks_image.subsurface(pygame.Rect(192, 67, 64, 58))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        ROCK_THREE.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
        # ROCK_THREE.add_component(BoxCollider2D("Box-3"))

        ISLAND = GameObject("Island", Transform2D(Vector2(0, 0), 0, Vector2(3.5, 3)), GameObjectType.Static,
                            GameObjectCategory.Environment)
        object_frame = image2.subsurface(pygame.Rect(29, 285, 158, 80))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        ISLAND.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))

    class UnnaturalStructures:
        structures_layer = RendererLayers.BelowPlayer

        BUILDING = GameObject("Building", Transform2D(Vector2(0, 0), 0, Vector2(0.1, 0.1)), GameObjectType.Static,
                              GameObjectCategory.Environment)
        object_frame = building_image
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        BUILDING.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
        BUILDING.add_component(BoxCollider2D("Box-3"))

        DOOR = GameObject("Door", Transform2D(Vector2(0, 0), 0, Vector2(1, 1)), GameObjectType.Static,
                          GameObjectCategory.Environment)
        object_frame = door_image
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        DOOR.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
        DOOR.add_component(BoxCollider2D("Box-3"))

        WINDOW = GameObject("Window", Transform2D(Vector2(0, 0), 0, Vector2(1, 1)), GameObjectType.Static,
                            GameObjectCategory.Environment)
        object_frame = window_image
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        WINDOW.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))

        BED = GameObject("Bed", Transform2D(Vector2(0, 0), 0, Vector2(1, 1)), GameObjectType.Static,
                         GameObjectCategory.Environment)
        object_frame = bed_image
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        BED.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
        BED.add_component(BoxCollider2D("Box-3"))

        TABLE = GameObject("Table", Transform2D(Vector2(0, 0), 0, Vector2(1, 1)), GameObjectType.Static,
                           GameObjectCategory.Environment)
        object_frame = table_image
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        TABLE.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))

        COUCH = GameObject("Table", Transform2D(Vector2(0, 0), 0, Vector2(1, 1)), GameObjectType.Static,
                           GameObjectCategory.Environment)
        object_frame = couch_image
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        COUCH.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
        COUCH.add_component(BoxCollider2D("Box-3"))

        # Earth Ruins
        RUIN_ONE = GameObject("RuinOne", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                              GameObjectCategory.Player)
        object_frame = ruins_image.subsurface(pygame.Rect(307, 293, 97, 103))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        RUIN_ONE.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
        RUIN_ONE.add_component(BoxCollider2D("Box-3"))

        RUIN_TWO = GameObject("RuinTwo", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                              GameObjectCategory.Player)
        object_frame = ruins_image.subsurface(pygame.Rect(202, 290, 101, 107))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        RUIN_TWO.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
        RUIN_TWO.add_component(BoxCollider2D("Box-3"))

        RUIN_THREE = GameObject("RuinTwo", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                                GameObjectCategory.Player)
        object_frame = ruins_image.subsurface(pygame.Rect(391, 2, 99, 118))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        RUIN_THREE.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
        RUIN_THREE.add_component(BoxCollider2D("Box-3"))

        # Mars Ruins

        RUIN_FOUR = GameObject("RuinTwo", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                               GameObjectCategory.Player)
        object_frame = ruins_image.subsurface(pygame.Rect(388, 168, 54, 48))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        RUIN_FOUR.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
        RUIN_FOUR.add_component(BoxCollider2D("Box-3"))

        RUIN_FIVE = GameObject("RuinTwo", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                               GameObjectCategory.Player)
        object_frame = ruins_image.subsurface(pygame.Rect(226, 67, 73, 68))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        RUIN_FIVE.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
        RUIN_FIVE.add_component(BoxCollider2D("Box-3"))

        RUIN_SIX = GameObject("RuinTwo", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                              GameObjectCategory.Player)
        object_frame = ruins_image.subsurface(pygame.Rect(91, 295, 99, 96))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        RUIN_SIX.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
        RUIN_SIX.add_component(BoxCollider2D("Box-3"))

        # Saturn Ruins

        RUIN_SEVEN = GameObject("RuinTwo", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                                GameObjectCategory.Player)
        object_frame = ruins_image.subsurface(pygame.Rect(4, 3, 53, 57))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        RUIN_SEVEN.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))

        RUIN_EIGHT = GameObject("RuinTwo", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                                GameObjectCategory.Player)
        object_frame = ruins_image.subsurface(pygame.Rect(296, 199, 82, 81))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        RUIN_EIGHT.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))

        RUIN_NINE = GameObject("RuinTwo", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                               GameObjectCategory.Player)
        object_frame = ruins_image.subsurface(pygame.Rect(3, 368, 69, 64))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        RUIN_NINE.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))

        STATUE = GameObject("Statue", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                            GameObjectCategory.Player)
        object_frame = ruins_image.subsurface(pygame.Rect(341, 1, 42, 60))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        STATUE.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
        # STATUE.add_component(BoxCollider2D("Box-3"))

        BRIDGE = GameObject("Bridge", Transform2D(Vector2(0, 0), 0, Vector2(3, 3)), GameObjectType.Static,
                            GameObjectCategory.Environment)
        object_frame = image2.subsurface(pygame.Rect(217, 292, 47, 31))
        texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
        BRIDGE.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))

    class Consumables:
        layer = RendererLayers.WorldObjects
        __POTION_SCALE = 0.4

        POTION_SPEED = PowerUp("PotionSpeed", PowerUpType.Speed,
                               Transform2D(Vector2(0, 0), 0, Vector2(__POTION_SCALE, __POTION_SCALE)),
                               GameObjectType.Static, GameObjectCategory.PowerUp)
        texture_material = GameConstants.PowerUp.MATERIAL_POTION_SPEED
        POTION_SPEED.add_component(SpriteRenderer2D("Renderer-2", texture_material, layer))
        POTION_SPEED.add_component(PowerUpCollider("Potion Speed Collider"))
        POTION_SPEED.add_component(SpriteAnimator2D("Potion", GameConstants.PowerUp.POWER_UP_ANIMATOR_INFO,
                                                    texture_material, ActiveTake.POTION,
                                                    GameConstants.PowerUp.ANIMATION_SPEED))

        POTION_ATTACK = PowerUp("PotionAttack", PowerUpType.Attack,
                                Transform2D(Vector2(0, 0), 0, Vector2(__POTION_SCALE, __POTION_SCALE)))
        texture_material = GameConstants.PowerUp.MATERIAL_POTION_ATTACK
        POTION_ATTACK.add_component(SpriteRenderer2D("Renderer-2", texture_material, layer))
        POTION_ATTACK.add_component(PowerUpCollider("Potion Speed Collider"))
        POTION_ATTACK.add_component(SpriteAnimator2D("Potion", GameConstants.PowerUp.POWER_UP_ANIMATOR_INFO,
                                                     texture_material, ActiveTake.POTION,
                                                     GameConstants.PowerUp.ANIMATION_SPEED))

        POTION_DEFENSE = PowerUp("PotionDefense", PowerUpType.Defense,
                                 Transform2D(Vector2(0, 0), 0, Vector2(__POTION_SCALE, __POTION_SCALE)))
        texture_material = GameConstants.PowerUp.MATERIAL_POTION_DEFENSE
        POTION_DEFENSE.add_component(SpriteRenderer2D("Renderer-2", texture_material, layer))
        POTION_DEFENSE.add_component(PowerUpCollider("Potion Attack Collider"))
        POTION_DEFENSE.add_component(SpriteAnimator2D("Potion", GameConstants.PowerUp.POWER_UP_ANIMATOR_INFO,
                                                      texture_material, ActiveTake.POTION,
                                                      GameConstants.PowerUp.ANIMATION_SPEED))

        POTION_HEAL = PowerUp("PotionHeal", PowerUpType.Heal,
                              Transform2D(Vector2(0, 0), 0, Vector2(__POTION_SCALE, __POTION_SCALE)))
        texture_material = GameConstants.PowerUp.MATERIAL_POTION_HEAL
        POTION_HEAL.add_component(SpriteRenderer2D("Renderer-2", texture_material, layer))
        POTION_HEAL.add_component(PowerUpCollider("Potion Heal Collider"))
        POTION_HEAL.add_component(SpriteAnimator2D("Potion", GameConstants.PowerUp.POWER_UP_ANIMATOR_INFO,
                                                   texture_material, ActiveTake.POTION,
                                                   GameConstants.PowerUp.ANIMATION_SPEED))

        RANDOM_POWER_UP = PowerUp("RandomPowerUp", PowerUpType.Random,
                                  Transform2D(Vector2(0, 0), 0, Vector2(__POTION_SCALE, __POTION_SCALE)))
        texture_material = GameConstants.PowerUp.MATERIAL_RANDOM
        RANDOM_POWER_UP.add_component(SpriteRenderer2D("Renderer-2", texture_material, layer))
        RANDOM_POWER_UP.add_component(PowerUpCollider("Random Power Up Collider"))
        RANDOM_POWER_UP.add_component(SpriteAnimator2D("Random", GameConstants.PowerUp.POWER_UP_ANIMATOR_INFO,
                                                       texture_material, ActiveTake.RANDOM,
                                                       GameConstants.PowerUp.ANIMATION_SPEED))

        NIGHT_VISION_POWER_UP = PowerUp("NightVisionPowerUp", PowerUpType.NightVision,
                                        Transform2D(Vector2(0, 0), 0, Vector2(__POTION_SCALE, __POTION_SCALE)))
        texture_material = GameConstants.PowerUp.MATERIAL_NIGHT_VISION
        NIGHT_VISION_POWER_UP.add_component(SpriteRenderer2D("Renderer-2", texture_material, layer))
        RANDOM_POWER_UP.add_component(PowerUpCollider("Night Vision Collider"))
        NIGHT_VISION_POWER_UP.add_component(
            SpriteAnimator2D("NightVision", GameConstants.PowerUp.POWER_UP_ANIMATOR_INFO,
                             texture_material, ActiveTake.NIGHT_VISION,
                             GameConstants.PowerUp.ANIMATION_SPEED))

    class Gun:
        texture = pygame.image.load("Assets/SpriteSheets/fire_ball_image.png")

        material = TextureMaterial2D(texture, None, None, 255)

        colors = [None]
        bullet_prefab = Bullet("Bullet", material, 1, 15, Transform2D(Vector2(0, 0), 0, Vector2(0.1, 0.1)))
        Gun = Gun("Gun", bullet_prefab, 1.5, colors, Transform2D(Vector2(2400, 4500), 0, Vector2(0.2, 0.2)))

    class Cameras:
        __MAIN_MENU_CAMERA_COMPONENT = Camera(GameConstants.Cameras.MENU_CAMERA, GameConstants.VIEWPORT_WIDTH,
                                              GameConstants.VIEWPORT_HEIGHT)
        MAIN_MENU_CAMERA = GameObject(GameConstants.Cameras.MENU_CAMERA,
                                      Transform2D(Vector2(0, 0), Vector2(0, 0), Vector2(0, 0)), GameObjectType.Static,
                                      GameObjectCategory.Menu)
        MAIN_MENU_CAMERA.add_component(__MAIN_MENU_CAMERA_COMPONENT)

        GAME_CAMERA = MAIN_MENU_CAMERA.clone()
        GAME_CAMERA.get_component(Camera).name = GameConstants.Cameras.GAME_CAMERA
        GAME_CAMERA.name = GameConstants.Cameras.GAME_CAMERA

    class UiHelperTexts:
        UI_HELPER_TEXT_FONT_PATH = "Assets/Fonts/VCR_OSD_MONO.ttf"
        UI_TEXT_HELPER_BOTTOM = GameObject(GameConstants.UITextPrompts.UI_TEXT_BOTTOM,
                                           Transform2D(Vector2(0, 0), 0, Vector2(1, 1)),
                                           GameObjectType.Static, GameObjectCategory.UIPrompts)
        UI_TEXT_HELPER_RIGHT = UI_TEXT_HELPER_BOTTOM.clone()
        UI_TEXT_HELPER_RIGHT.name = GameConstants.UITextPrompts.UI_TEXT_RIGHT
        UI_TEXT_HELPER_RIGHT2 = UI_TEXT_HELPER_BOTTOM.clone()
        UI_TEXT_HELPER_RIGHT2.name = GameConstants.UITextPrompts.UI_TEXT_RIGHT2
        UI_HELPER_TEXTS = (UI_TEXT_HELPER_BOTTOM, UI_TEXT_HELPER_RIGHT, UI_TEXT_HELPER_RIGHT2)

    class HealthBar:
        __HEALTH_BAR_IMAGE_BASE_PATH = "Assets/UI/HealthBars/"
        __HEALTH_BAR_IMAGE_END_PATH = "_health_bar.png"

        __PLAYER_HEALTH_BAR_IMAGE = pygame.image.load(
            __HEALTH_BAR_IMAGE_BASE_PATH + "player" + __HEALTH_BAR_IMAGE_END_PATH)
        RAT_ENEMY_HEALTH_BAR_IMAGE = pygame.image.load(
            __HEALTH_BAR_IMAGE_BASE_PATH + "rat" + __HEALTH_BAR_IMAGE_END_PATH)
        WOLF_ENEMY_HEALTH_BAR_IMAGE = pygame.image.load(
            __HEALTH_BAR_IMAGE_BASE_PATH + "wolf" + __HEALTH_BAR_IMAGE_END_PATH)
        ALIEN_ENEMY_HEALTH_BAR_IMAGE = pygame.image.load(
            __HEALTH_BAR_IMAGE_BASE_PATH + "alien" + __HEALTH_BAR_IMAGE_END_PATH)

        __PLAYER_MATERIAL_HEALTH_BAR = TextureMaterial2D(__PLAYER_HEALTH_BAR_IMAGE, None, Vector2(0, 0), None)
        __ENEMY_MATERIAL_HEALTH_BAR = TextureMaterial2D(ALIEN_ENEMY_HEALTH_BAR_IMAGE, None, Vector2(0, 0), None)

        __RECT_MATERIAL_PLAYER_HEALTH_BAR_BACKGROUND = RectMaterial2D(375, 50, (0, 0, 0), 255, Vector2(135, 63))
        __RECT_MATERIAL_PLAYER_HEALTH_BAR = RectMaterial2D(375, 50, (0, 224, 79), 255, Vector2(135, 63))

        __RECT_MATERIAL_ENEMY_HEALTH_BAR_BACKGROUND = RectMaterial2D(375, 50, (0, 0, 0), 255, Vector2(58, 28))
        __RECT_MATERIAL_ENEMY_HEALTH_BAR = RectMaterial2D(375, 50, (0, 224, 79), 255, Vector2(58, 28))

        PLAYER_HEALTH_BAR = GameObject("Health Bar", Transform2D(Vector2(0, -15), 0, Vector2(0.7, 0.7)),
                                       GameObjectType.Static, GameObjectCategory.UI)

        PLAYER_HEALTH_BAR.add_component(
            Renderer2D("Health Bar Renderer Texture", __PLAYER_MATERIAL_HEALTH_BAR, RendererLayers.UIHealthBar))
        PLAYER_HEALTH_BAR.add_component(
            Renderer2D("Health Bar Renderer Rect Background", __RECT_MATERIAL_PLAYER_HEALTH_BAR_BACKGROUND,
                       RendererLayers.UIBackground))
        PLAYER_HEALTH_BAR.add_component(
            Renderer2D("Health Bar Renderer Rect", __RECT_MATERIAL_PLAYER_HEALTH_BAR, RendererLayers.UI))

        ENEMY_HEALTH_BAR = GameObject("Enemy Health Bar", Transform2D(Vector2(0, 0), 0, Vector2(0.3, 0.3)),
                                      GameObjectType.Dynamic, GameObjectCategory.EnemyHealthUI)
        ENEMY_HEALTH_BAR.add_component(
            Renderer2D("Health Bar Renderer Texture", __ENEMY_MATERIAL_HEALTH_BAR, RendererLayers.UIHealthBar, False))
        ENEMY_HEALTH_BAR.add_component(
            Renderer2D("Health Bar Renderer Rect Background", __RECT_MATERIAL_ENEMY_HEALTH_BAR_BACKGROUND,
                       RendererLayers.UIBackground, False))
        ENEMY_HEALTH_BAR.add_component(
            Renderer2D("Health Bar Renderer Rect", __RECT_MATERIAL_ENEMY_HEALTH_BAR, RendererLayers.UI, False))

    class Teleporter:
        __TELEPORTER_HEIGHT = 368
        __TELEPORTER_WIDTH = 117
        __TELEPORTER_Y = 1

        TELEPORTER_NAME = "Teleporter"

        __TELEPORTER_FRAME_RECTS = [
            pygame.Rect(52 - 19, __TELEPORTER_Y, __TELEPORTER_WIDTH, __TELEPORTER_HEIGHT),
            pygame.Rect(231 - 8, __TELEPORTER_Y, __TELEPORTER_WIDTH, __TELEPORTER_HEIGHT),
            pygame.Rect(421 - 8, __TELEPORTER_Y, __TELEPORTER_WIDTH, __TELEPORTER_HEIGHT),
            pygame.Rect(611 - 8, __TELEPORTER_Y, __TELEPORTER_WIDTH, __TELEPORTER_HEIGHT),
            pygame.Rect(812 - 19, __TELEPORTER_Y, __TELEPORTER_WIDTH, __TELEPORTER_HEIGHT),
            pygame.Rect(1002 - 19, __TELEPORTER_Y, __TELEPORTER_WIDTH, __TELEPORTER_HEIGHT),
            pygame.Rect(1192 - 19, __TELEPORTER_Y, __TELEPORTER_WIDTH, __TELEPORTER_HEIGHT),
            pygame.Rect(1380 - 17, __TELEPORTER_Y, __TELEPORTER_WIDTH, __TELEPORTER_HEIGHT),
            pygame.Rect(1553, __TELEPORTER_Y, __TELEPORTER_WIDTH, __TELEPORTER_HEIGHT),
            pygame.Rect(1744 - 1, __TELEPORTER_Y, __TELEPORTER_WIDTH, __TELEPORTER_HEIGHT),
            pygame.Rect(1934 - 1, __TELEPORTER_Y, __TELEPORTER_WIDTH, __TELEPORTER_HEIGHT),
            pygame.Rect(2124 - 1, __TELEPORTER_Y, __TELEPORTER_WIDTH, __TELEPORTER_HEIGHT),
            pygame.Rect(2314 - 1, __TELEPORTER_Y, __TELEPORTER_WIDTH, __TELEPORTER_HEIGHT),
            pygame.Rect(2522 - 19, __TELEPORTER_Y, __TELEPORTER_WIDTH, __TELEPORTER_HEIGHT)
        ]
        __TELEPORTER = Take(ActiveTake.TELEPORT, __TELEPORTER_FRAME_RECTS, False, 1)

        __TELEPORTER_IDLE_FRAME_RECT = [pygame.Rect(52 - 19, __TELEPORTER_Y, __TELEPORTER_WIDTH, __TELEPORTER_HEIGHT)]

        __TELEPORTER_IDLE = Take(ActiveTake.TELEPORT_IDLE, __TELEPORTER_IDLE_FRAME_RECT)

        TELEPORTER_ANIMATION_INFO = [__TELEPORTER, __TELEPORTER_IDLE]

        __TELEPORTER_SPRITE_SHEET = pygame.image.load("Assets/SpriteSheets/teleporter.png")

        MATERIAL_TELEPORTER = TextureMaterial2D(__TELEPORTER_SPRITE_SHEET, None, Vector2(0, 0), None)

        TELEPORTER = GameObject(TELEPORTER_NAME, Transform2D(Vector2(0, 0), 0, Vector2(1, 1)), GameObjectType.Static,
                                GameObjectCategory.Teleporter)

        TELEPORTER.add_component(
            SpriteAnimator2D("Teleporter Sprite Animator", TELEPORTER_ANIMATION_INFO, MATERIAL_TELEPORTER,
                             ActiveTake.TELEPORT_IDLE, 4))
        TELEPORTER.add_component(SpriteRenderer2D("Renderer-2", MATERIAL_TELEPORTER, RendererLayers.WorldObjects))
        teleporter_box_collider = BoxCollider2D("Teleporter Box Collider")
        teleporter_box_collider.scale = Vector2(4, 1)
        TELEPORTER.add_component(teleporter_box_collider)
        TELEPORTER.add_component(TeleporterCollider("Teleporter Collider"))
