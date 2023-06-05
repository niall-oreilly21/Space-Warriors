from random import randint

import pygame
from pygame import Vector2

from App.Components.Colliders.TreeBoxCollider2D import TreeBoxCollider2D
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.GameObject import GameObject
from Engine.Graphics.Materials.TextureMaterial2D import TextureMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Sprites.Take import Take
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Enums.GameObjectEnums import GameObjectType, GameObjectCategory
from Engine.Other.Transform2D import Transform2D
from Engine.Other.Enums.RendererLayers import RendererLayers

tp_image = pygame.image.load("Assets/SpriteSheets/Tilesets/Obelisk.png")
image = pygame.image.load("Assets/SpriteSheets/Tilesets/plain_tileset.png")
ruins_image = pygame.image.load("Assets/SpriteSheets/Tilesets/Assets_source.png")
rocks_image = pygame.image.load("Assets/SpriteSheets/Tilesets/Rocks_source.png")
bushes_image = pygame.image.load("Assets/SpriteSheets/Tilesets/Bushes_source.png")
image2 = pygame.image.load("Assets/SpriteSheets/Tilesets/plain_tileset2.png")


class GameObjectConstants:
    layer = RendererLayers.WorldObjects
    tree_layer = RendererLayers.AbovePlayer
    structures_layer = RendererLayers.BelowPlayer

    tree_collider = TreeBoxCollider2D("TreeCollider")


    TELEPORTER = GameObject("Teleporter", Transform2D(Vector2(0, 0), 0, Vector2(1, 1)), GameObjectType.Dynamic,
                            GameObjectCategory.Environment)
    object_frame = tp_image.subsurface(pygame.Rect(52, 23, 79, 204))
    texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
    TELEPORTER.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
    TELEPORTER.add_component(tree_collider)

    TALL_TREE = GameObject("Tree", Transform2D(Vector2(0, 0), 0, Vector2(3, 3)), GameObjectType.Static,
                           GameObjectCategory.Environment)
    object_frame = image.subsurface(pygame.Rect(179, 98, 27, 60))
    texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
    tree_renderer = Renderer2D("Renderer-2", texture_material, tree_layer)
    TALL_TREE.add_component(tree_renderer)
    TALL_TREE.add_component(tree_collider)

    LOW_TREE = GameObject("LowTree", Transform2D(Vector2(0, 0), 0, Vector2(3, 3)), GameObjectType.Static,
                          GameObjectCategory.Environment)
    object_frame = image.subsurface(pygame.Rect(177, 65, 30, 30))
    texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
    LOW_TREE.add_component(Renderer2D("Renderer-2", texture_material, tree_layer))
    LOW_TREE.add_component(tree_collider)


    BOULDER = GameObject("Boulder", Transform2D(Vector2(0, 0), 0, Vector2(3, 3)), GameObjectType.Static,
                         GameObjectCategory.Environment)
    object_frame = image.subsurface(pygame.Rect(129, 146, 13, 12))
    texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
    BOULDER.add_component(Renderer2D("Renderer-2", texture_material, layer))
    # BOULDER.add_component(BoxCollider2D("Box-3"))

    BOULDER_TWO = GameObject("BoulderTwo", Transform2D(Vector2(0, 0), 0, Vector2(3, 3)), GameObjectType.Static,
                             GameObjectCategory.Environment)
    object_frame = ruins_image.subsurface(pygame.Rect(148, 145, 40, 42))
    texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
    BOULDER_TWO.add_component(Renderer2D("Renderer-2", texture_material, layer))
    # BOULDER_TWO.add_component(BoxCollider2D("Box-3"))

    RUIN_ONE = GameObject("RuinOne", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                          GameObjectCategory.Environment)
    object_frame = ruins_image.subsurface(pygame.Rect(307, 293, 97, 103))
    texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
    RUIN_ONE.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
    # RUIN_ONE.add_component(BoxCollider2D("Box-3"))

    RUIN_TWO = GameObject("RuinTwo", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                          GameObjectCategory.Environment)
    object_frame = ruins_image.subsurface(pygame.Rect(9, 193, 67, 92))
    texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
    RUIN_TWO.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
    # RUIN_TWO.add_component(BoxCollider2D("Box-3"))

    STATUE = GameObject("Statue", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                        GameObjectCategory.Environment)
    object_frame = ruins_image.subsurface(pygame.Rect(341, 1, 42, 60))
    texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
    STATUE.add_component(Renderer2D("Renderer-2", texture_material, structures_layer))
    # STATUE.add_component(BoxCollider2D("Box-3"))

    ROCK_ONE = GameObject("RockOne", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                          GameObjectCategory.Environment)
    object_frame = rocks_image.subsurface(pygame.Rect(193, 6, 62, 52))
    texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
    ROCK_ONE.add_component(Renderer2D("Renderer-2", texture_material, layer))
    ROCK_ONE.add_component(BoxCollider2D("Box-3"))

    ROCK_TWO = GameObject("RockTwo", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                          GameObjectCategory.Environment)
    object_frame = rocks_image.subsurface(pygame.Rect(67, 2, 58, 57))
    texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
    ROCK_TWO.add_component(Renderer2D("Renderer-2", texture_material, layer))
    ROCK_TWO.add_component(BoxCollider2D("Box-3"))

    ROCK_THREE = GameObject("RockThree", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                            GameObjectCategory.Environment)
    object_frame = rocks_image.subsurface(pygame.Rect(192, 67, 64, 58))
    texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
    ROCK_THREE.add_component(Renderer2D("Renderer-2", texture_material, layer))
    ROCK_THREE.add_component(BoxCollider2D("Box-3"))

    BUSH_ONE = GameObject("BushOne", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                          GameObjectCategory.Environment)
    object_frame = bushes_image.subsurface(pygame.Rect(295, 7, 36, 32))
    texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
    BUSH_ONE.add_component(Renderer2D("Renderer-2", texture_material, layer))
    BUSH_ONE.add_component(BoxCollider2D("BushCollider"))

    BUSH_TWO = GameObject("BushTwo", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                          GameObjectCategory.Environment)
    object_frame = bushes_image.subsurface(pygame.Rect(244, 6, 40, 34))
    texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
    BUSH_TWO.add_component(Renderer2D("Renderer-2", texture_material, layer))
    BUSH_TWO.add_component(BoxCollider2D("BushCollider"))


    BUSH_THREE = GameObject("BushThree", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                            GameObjectCategory.Environment)
    object_frame = bushes_image.subsurface(pygame.Rect(56, 6, 31, 29))
    texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
    BUSH_THREE.add_component(Renderer2D("Renderer-2", texture_material, layer))
    BUSH_THREE.add_component(BoxCollider2D("BushCollider"))


    BUSH_FOUR = GameObject("BushFour", Transform2D(Vector2(0, 0), 0, Vector2(2, 2)), GameObjectType.Static,
                           GameObjectCategory.Environment)
    object_frame = bushes_image.subsurface(pygame.Rect(196, 6, 39, 37))
    texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
    BUSH_FOUR.add_component(Renderer2D("Renderer-2", texture_material, layer))
    BUSH_FOUR.add_component(BoxCollider2D("BushCollider"))


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

    ISLAND = GameObject("Island", Transform2D(Vector2(0, 0), 0, Vector2(3.5, 3)), GameObjectType.Static,
                        GameObjectCategory.Environment)
    object_frame = image2.subsurface(pygame.Rect(29, 285, 158, 80))
    texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
    ISLAND.add_component(Renderer2D("Renderer-2", texture_material, layer))

    BRIDGE = GameObject("Bridge", Transform2D(Vector2(0, 0), 0, Vector2(3, 3)), GameObjectType.Static,
                        GameObjectCategory.Environment)
    object_frame = image2.subsurface(pygame.Rect(217, 292, 47, 31))
    texture_material = TextureMaterial2D(object_frame, None, Vector2(0, 0), 255)
    BRIDGE.add_component(Renderer2D("Renderer-2", texture_material, layer))
