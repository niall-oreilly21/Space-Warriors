import json
import random

from pygame import Vector2

from App.Components.Controllers.EnemyController import EnemyController
from App.Constants.Constants import Constants
from App.Constants.EntityConstants import EntityConstants
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
from Engine.Other.Enums.RendererLayers import RendererLayers
from Engine.Other.Transform2D import Transform2D


def map_load(scene, planet_json,player):
    tileset = Tileset("Assets/SpriteSheets/Tilesets/plain_tileset2.png", 36, 36)

    # Add tiles to the tileset
    tileset.add_tile(Tile("Grass", Constants.Tile.GRASS, Vector2(216, 12)))
    tileset.add_tile(Tile("Water", Constants.Tile.WATER, Vector2(264, 156)))
    tileset.add_tile(Tile("Dark Grass", Constants.Tile.DARK_GRASS, Vector2(216, 108)))
    tileset.add_tile(Tile("Dirt", Constants.Tile.DIRT, Vector2(308, 12)))
    tileset.add_tile(Tile("Sand", Constants.Tile.SAND, Vector2(216, 156)))
    # tileset.add_tile(Tile("Dirt", 7, Vector2(216, 156)))
    tileset.add_tile(Tile("CoarseDirt", Constants.Tile.COARSE_DIRT, Vector2(216, 108)))
    tileset.add_tile(Tile("SaturnDirt", 10, Vector2(308,12)))
    tileset.add_tile(Tile("SaturnSand", 7, Vector2(216, 156)))
    tileset.add_tile(Tile("SaturnSpawnRegion", 4, Vector2(216, 108)))

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
        load_planet_a_specifics(scene, player)
        color_tiles(map_data, tile_data, width, height, None, None)
    elif scene.name == Constants.Scene.MARS:
        load_planet_b_specifics(scene,player)
        color_tiles(map_data, tile_data, width, height, [200, 40, 40], 220)
    elif scene.name == Constants.Scene.SATURN:
        load_planet_c_specifics(scene,player)
        color_tiles(map_data, tile_data, width, height, [100,100,100], 200)

    # Object generation
    for object in object_data:
        if object["x"] < width and object["y"] < height:
            x = object["x"]
            y = object["y"]
            c_value = object["c"]
            id = object["t"]["id"]
            if id == 5:
                tree_object = random.choice(
                    [GameObjectConstants.Foliage.TALL_TREE.clone(), GameObjectConstants.Foliage.LOW_TREE.clone()])
                tree_collider = BoxCollider2D("TreeCollider")
                if tree_object.name == "Tree":
                    tree_collider.scale = Vector2(0.3, 0.15)
                    tree_collider.offset = Vector2(3, 72)
                else:
                    tree_collider.scale = Vector2(0.5, 0.25)
                    tree_collider.offset = Vector2(0, 32)
                tree_object.add_component(tree_collider)
                tree_object.transform.position = Vector2(x * 71, y * 71)  # starting area forces every tree to one point
                scene.add(tree_object)
            elif id == 15:
                bush_object = random.choice([GameObjectConstants.Foliage.BUSH_ONE.clone(), GameObjectConstants.Foliage.BUSH_TWO.clone(),
                                             GameObjectConstants.Foliage.BUSH_FOUR.clone(),
                                             GameObjectConstants.NaturalStructures.ROCK_ONE.clone()])
                bush_object.add_component(BoxCollider2D("BushCollider"))
                if bush_object.name == "RockOne":
                    scale = random.uniform(0.7, 2)
                    bush_object.transform.scale = Vector2(scale, scale)
                bush_object.transform.position = Vector2(x * 72, y * 72)

                scene.add(bush_object)
            elif id == 11:
                lilypad_object = random.choice([GameObjectConstants.Foliage.LILYPAD_ONE.clone(),
                                                GameObjectConstants.Foliage.LILYPAD_TWO.clone()])
                lilypad_object.transform.rotation = random.randint(0, 360)
                lilypad_object.transform.position = Vector2(x * 72.5, y * 72.5)

                scene.add(lilypad_object)
            elif id == 1:
                power_up_object = random.choice([GameObjectConstants.Consumables.POTION_SPEED.clone(),
                                                 GameObjectConstants.Consumables.POTION_HEAL.clone(),
                                                 GameObjectConstants.Consumables.POTION_ATTACK.clone(),
                                                 GameObjectConstants.Consumables.POTION_DEFENSE.clone(),
                                                 GameObjectConstants.Consumables.RANDOM_POWER_UP.clone()])
                power_up_object.transform.position = Vector2(x * 72.5, y * 72.5)
                power_up_collider = BoxCollider2D("PowerUpCollider")
                power_up_collider.scale = Vector2(2.5, 2.5)
                power_up_object.add_component(power_up_collider)
                scene.add(power_up_object)



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


    # enemy_texture = Constants.EnemyRat.MATERIAL_ENEMY1
    # load_enemy_1(player, enemy_texture, 2400,3400)

def color_tiles(map_data, tile_data, width, height, color, alpha):
    # Create Default Tiles
    for x in range(height):
        row = []
        for z in range(width):
            tile = TileAttributes(Constants.Tile.WATER, False, color, alpha)
            row.append(tile)
        map_data.append(row)

    for ground in tile_data:
        if ground["x"] < width and ground["y"] < height:
            x = ground["x"]
            y = ground["y"]
            s_id = ground["s"]["id"]
            if s_id == Constants.Tile.WATER:
                map_data[y][x] = TileAttributes(s_id, True, color, alpha)
            # elif s_id == Constants.Tile.SAND:
            #     map_data[y][x] = TileAttributes(Constants.Tile.SAND, False, color, c_value)
            else:
                map_data[y][x] = TileAttributes(s_id, False, color, alpha)








def load_planet_a_specifics(scene, player):
    starting_pos = Vector2(2900, 4900)

    player.transform.position = starting_pos

    enemy = EntityConstants.Enemy.wolf
    scene.add(enemy)
    enemy.add_component(EnemyController("Enemy movement", player, Constants.EnemyWolf.MOVE_SPEED, 200))

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

    statue = GameObjectConstants.UnnaturalStructures.STATUE.clone()
    statue.transform.position = Vector2(2900, 4700)
    scene.add(statue)

    planet_a_first_house = Vector2(2200, 2000)
    first_boss_coords = Vector2(6000, 1500)

    teleporter = GameObjectConstants.Teleporter.TELEPORTER
    teleporter.transform.position = Vector2(2500, 4800)
    scene.add(teleporter)

    bridge_x = 6406
    bridge_y = 5463

    island = GameObjectConstants.NaturalStructures.ISLAND.clone()
    island.transform.position = Vector2(bridge_x + 47 * 7 + 22, bridge_y - 45)
    scene.add(island)

    bridge = GameObjectConstants.UnnaturalStructures.BRIDGE.clone()
    bridge.transform.position = Vector2(bridge_x, bridge_y)
    scene.add(bridge)

    bridge2 = GameObjectConstants.UnnaturalStructures.BRIDGE.clone()
    bridge2.transform.position = Vector2(bridge_x + 47, bridge_y)
    scene.add(bridge2)

    bridge3 = GameObjectConstants.UnnaturalStructures.BRIDGE.clone()
    bridge3.transform.position = Vector2(bridge_x + 47 * 3, bridge_y)
    scene.add(bridge3)

    bridge4 = GameObjectConstants.UnnaturalStructures.BRIDGE.clone()
    bridge4.transform.position = Vector2(bridge_x + 47 * 5, bridge_y)
    scene.add(bridge4)

    # enemies
    # load_enemy_1(player,Constants.E)




def load_planet_b_specifics(scene,player):
    starting_pos = Vector2(3639.8, 4705.6)
    player.transform.position = starting_pos
    scene.add(player)

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

    statue = GameObjectConstants.UnnaturalStructures.STATUE.clone()
    statue.transform.position = Vector2(2900, 4700)
    scene.add(statue)

    planet_b_first_house = Vector2(2200, 2000)
    first_boss_coords = Vector2(6000, 1500)

    # teleporter = GameObjectConstants.Teleporter.TELEPORTER.clone()
    # teleporter.transform.position = Vector2(2500, 5000)
    # scene.add(teleporter)

def load_planet_c_specifics(scene, player):
    starting_pos = Vector2(919.8, 6298)
    player.transform.position = starting_pos
    scene.add(player)
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

    statue = GameObjectConstants.UnnaturalStructures.STATUE.clone()
    statue.transform.position = Vector2(2900, 4700)
    scene.add(statue)

    planet_a_first_house = Vector2(2200, 2000)
    first_boss_coords = Vector2(6000, 1500)

    # teleporter = GameObjectConstants.Teleporter.TELEPORTER.clone()
    # teleporter.transform.position = Vector2(2500, 5000)
    # scene.add(teleporter)


















