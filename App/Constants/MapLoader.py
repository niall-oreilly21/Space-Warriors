import json
import random

from pygame import Vector2

from App.Components.Colliders.TreeBoxCollider2D import TreeBoxCollider2D
from App.Components.Controllers.EnemyController import EnemyController
from App.Constants.Application import Application
from App.Constants.Constants import Constants
from Engine.Other.Enums.RendererLayers import RendererLayers
from App.Constants.GameObjectConstants import GameObjectConstants
from Engine.GameObjects.Character import Character
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.GameObjects.Tiles.Tile import Tile
from Engine.GameObjects.Tiles.TileAttributes import TileAttributes
from Engine.GameObjects.Tiles.Tileset import Tileset
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Enums.GameObjectEnums import GameObjectType, GameObjectCategory
from Engine.Other.Enums.MapID import MapID
from Engine.Other.Transform2D import Transform2D


def map_load(scene, planet_json,player):
    tileset = Tileset("Assets/SpriteSheets/Tilesets/plain_tileset2.png", 36, 36)

    # Add tiles to the tileset
    tileset.add_tile(Tile("Grass", Constants.Tile.GRASS, Vector2(216, 12)))
    tileset.add_tile(Tile("Water", Constants.Tile.WATER, Vector2(264, 156)))
    tileset.add_tile(Tile("Dark Grass", Constants.Tile.DARK_GRASS, Vector2(216, 108)))
    tileset.add_tile(Tile("Dirt", Constants.Tile.DIRT, Vector2(306, 12)))
    tileset.add_tile(Tile("Sand", Constants.Tile.SAND, Vector2(216, 156)))
    # tileset.add_tile(Tile("Dirt", 7, Vector2(216, 156)))
    tileset.add_tile(Tile("CoarseDirt", Constants.Tile.COARSE_DIRT, Vector2(216, 108)))

    map_data = []

    # load map data
    file_path = planet_json

    with open(file_path, "r") as file:
        json_data = json.load(file)

    tile_data = json_data["grounds"]
    object_data = json_data["objects"]

    width = 110
    height = 120


    # update tiles that are available, and color them, everything else default
    if scene.name == Constants.Scene.EARTH:
        load_planet_a_specifics(scene)
        color_tiles(map_data, tile_data, width, height, [255, 100, 0])
    elif scene.name == Constants.Scene.MARS:
        load_planet_b_specifics(scene)
        color_tiles(map_data, tile_data, width, height, [255, 0, 0])
    elif scene.name == Constants.Scene.SATURN:
        load_planet_c_specifics(scene)
        color_tiles(map_data, tile_data, width, height, [255, 0, 0])

    # Object generation
    for object in object_data:
        if object["x"] < width and object["y"] < height:
            x = object["x"]
            y = object["y"]
            id = object["t"]["id"]
            if id == 5:
                tree_object = random.choice(
                    [GameObjectConstants.TALL_TREE.clone(), GameObjectConstants.LOW_TREE.clone()])
                tree_object.transform.position = Vector2(x * 71, y * 71)  # starting area forces every tree to one point
                scene.add(tree_object)
            elif id == 15:
                bush_object = random.choice([GameObjectConstants.BUSH_ONE.clone(), GameObjectConstants.BUSH_TWO.clone(),
                                             GameObjectConstants.BUSH_FOUR.clone(),
                                             GameObjectConstants.ROCK_ONE.clone()])
                if bush_object.name == "RockOne":
                    scale = random.uniform(0.7, 2)
                    bush_object.transform.scale = Vector2(scale, scale)
                bush_object.transform.position = Vector2(x * 72, y * 72)

                scene.add(bush_object)
            elif id == 11:
                lilypad_object = random.choice([GameObjectConstants.LILYPAD_ONE.clone(),
                                                GameObjectConstants.LILYPAD_TWO.clone()])
                lilypad_object.transform.rotation = random.randint(0, 360)
                lilypad_object.transform.position = Vector2(x * 72.5, y * 72.5)

                scene.add(lilypad_object)



    # Create the map using the tileset and map data
    map_tiles = tileset.create_map(map_data)

    # # Create the map using the tileset and map data
    # map_tiles = tileset.create_map(map_data)

    for tiles in map_tiles:
        for tile in tiles:
            tile.transform.scale = Vector2(2, 2)
            tile.transform.position *= 2
            # random_translation = Vector2(random.randint(1000, 2000), random.randint(10, 10))
            # tile.transform.translate_by(random_translation)
            scene.add(tile)
    scene.add(player)

    # enemy_texture = Constants.EnemyRat.MATERIAL_ENEMY1
    # load_enemy_1(player, enemy_texture, 2400,3400)

def color_tiles(map_data, tile_data, width, height, color):
    # Create Default Tiles
    for x in range(height):
        row = []
        for z in range(width):
            tile = TileAttributes(Constants.Tile.WATER, False, color, None)
            row.append(tile)
        map_data.append(row)

    for ground in tile_data:
        if ground["x"] < width and ground["y"] < height:
            x = ground["x"]
            y = ground["y"]
            c_value = ground["c"]
            s_id = ground["s"]["id"]
            if s_id == Constants.Tile.WATER:
                map_data[y][x] = TileAttributes(s_id, False, color, c_value)
            else:
                map_data[y][x] = TileAttributes(s_id, False, color, c_value)








def load_planet_a_specifics(scene):


    # ruin = GameObjectConstants.RUIN_ONE.clone()
    # ruin.transform.position = Vector2(2000,5000)
    # scene.add(ruin)
    #
    # ruin = GameObjectConstants.RUIN_TWO.clone()
    # ruin.transform.position = Vector2(1800,5000)
    # scene.add(ruin)
    #
    # boulder = GameObjectConstants.BOULDER_TWO.clone()
    # boulder.transform.position = Vector2(2200,5000)
    # scene.add(boulder)

    statue = GameObjectConstants.STATUE.clone()
    statue.transform.position = Vector2(2900, 4700)
    scene.add(statue)

    planet_a_first_house = Vector2(2200, 2000)
    first_boss_coords = Vector2(6000, 1500)

    teleporter = GameObjectConstants.TELEPORTER.clone()
    teleporter.transform.position = Vector2(2500, 5000)
    scene.add(teleporter)

    bridge_x = 6406
    bridge_y = 5475

    island = GameObjectConstants.ISLAND.clone()
    island.transform.position = Vector2(bridge_x + 47 * 7 + 22, bridge_y - 45)
    scene.add(island)

    bridge = GameObjectConstants.BRIDGE.clone()
    bridge.transform.position = Vector2(bridge_x, bridge_y)
    scene.add(bridge)

    bridge2 = GameObjectConstants.BRIDGE.clone()
    bridge2.transform.position = Vector2(bridge_x + 47, bridge_y)
    scene.add(bridge2)

    bridge3 = GameObjectConstants.BRIDGE.clone()
    bridge3.transform.position = Vector2(bridge_x + 47 * 3, bridge_y)
    scene.add(bridge3)

    bridge4 = GameObjectConstants.BRIDGE.clone()
    bridge4.transform.position = Vector2(bridge_x + 47 * 5, bridge_y)
    scene.add(bridge4)

def load_planet_b_specifics(scene):
    # ruin = GameObjectConstants.RUIN_ONE.clone()
    # ruin.transform.position = Vector2(2000,5000)
    # scene.add(ruin)
    #
    # ruin = GameObjectConstants.RUIN_TWO.clone()
    # ruin.transform.position = Vector2(1800,5000)
    # scene.add(ruin)
    #
    # boulder = GameObjectConstants.BOULDER_TWO.clone()
    # boulder.transform.position = Vector2(2200,5000)
    # scene.add(boulder)

    statue = GameObjectConstants.STATUE.clone()
    statue.transform.position = Vector2(2900, 4700)
    scene.add(statue)

    planet_a_first_house = Vector2(2200, 2000)
    first_boss_coords = Vector2(6000, 1500)

    teleporter = GameObjectConstants.TELEPORTER.clone()
    teleporter.transform.position = Vector2(2500, 5000)
    scene.add(teleporter)

def load_planet_c_specifics(scene):
    # ruin = GameObjectConstants.RUIN_ONE.clone()
    # ruin.transform.position = Vector2(2000,5000)
    # scene.add(ruin)
    #
    # ruin = GameObjectConstants.RUIN_TWO.clone()
    # ruin.transform.position = Vector2(1800,5000)
    # scene.add(ruin)
    #
    # boulder = GameObjectConstants.BOULDER_TWO.clone()
    # boulder.transform.position = Vector2(2200,5000)
    # scene.add(boulder)

    statue = GameObjectConstants.STATUE.clone()
    statue.transform.position = Vector2(2900, 4700)
    scene.add(statue)

    planet_a_first_house = Vector2(2200, 2000)
    first_boss_coords = Vector2(6000, 1500)

    teleporter = GameObjectConstants.TELEPORTER.clone()
    teleporter.transform.position = Vector2(2500, 5000)
    scene.add(teleporter)


def load_enemy_1(player, texture, x, y):
    enemy = Character("Enemy", 70, 100, 1, 1, Transform2D(Vector2(x, y), 0, Vector2(1.5, 1.5)),
                      GameObjectType.Dynamic,
                      GameObjectCategory.Rat)
    enemy.add_component(BoxCollider2D("Box-1"))
    enemy.add_component(Rigidbody2D("Rigid"))
    material_enemy = Constants.EnemyRat.MATERIAL_ENEMY1
    enemy.add_component(SpriteRenderer2D("enemy", material_enemy, RendererLayers.Enemy))
    enemy.add_component(SpriteAnimator2D("enemy", Constants.EnemyRat.ENEMY_ANIMATOR_INFO, material_enemy,
                                         ActiveTake.ENEMY_RAT_MOVE_DOWN, Constants.CHARACTER_MOVE_SPEED))
    enemy_controller = EnemyController("Enemy movement", player, Constants.EnemyRat.MOVE_SPEED)
    enemy.add_component(enemy_controller)


















