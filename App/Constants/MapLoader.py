import json
import random

from pygame import Vector2

from App.Constants.Constants import Constants
from App.Constants.GameObjectConstants import GameObjectConstants
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Tiles.Tile import Tile
from Engine.GameObjects.Tiles.TileAttributes import TileAttributes
from Engine.GameObjects.Tiles.Tileset import Tileset
from Engine.Other.Enums.MapID import MapID


def map_load(scene, planet_json):
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

    for x in range(110):
        row = []
        for z in range(120):
            tile = TileAttributes(Constants.Tile.WATER, False, None)
            row.append(tile)
        map_data.append(row)

    # More map data rows

    # update tiles that are available, everything else default
    for ground in tile_data:
        if ground["x"] < 100 and ground["y"] < 100:
            x = ground["x"]
            y = ground["y"]
            c_value = ground["c"]
            s_id = ground["s"]["id"]
            if s_id == Constants.Tile.WATER:
                map_data[y][x] = TileAttributes(s_id, False, c_value)
            else:
                map_data[y][x] = TileAttributes(s_id, False, c_value)

    # Object generation
    for object in object_data:
        if object["x"] < 100 and object["y"] < 100:
            x = object["x"]
            y = object["y"]
            c_value = object["c"]
            id = object["t"]["id"]
            if id == 5:
                tree_object = random.choice(
                    [GameObjectConstants.TALL_TREE.clone(), GameObjectConstants.LOW_TREE.clone()])
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
                bush_object = random.choice([GameObjectConstants.BUSH_ONE.clone(), GameObjectConstants.BUSH_TWO.clone(),
                                             GameObjectConstants.BUSH_FOUR.clone(),
                                             GameObjectConstants.ROCK_ONE.clone()])
                bush_object.add_component(BoxCollider2D("BushCollider"))
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
            elif id == 1:
                power_up_object = random.choice([GameObjectConstants.POTION_SPEED.clone(),
                                                 GameObjectConstants.POTION_HEAL.clone(),
                                                 GameObjectConstants.POTION_ATTACK.clone(),
                                                 GameObjectConstants.POTION_DEFENSE.clone(),
                                                 GameObjectConstants.RANDOM_POWER_UP.clone()])
                power_up_object.transform.position = Vector2(x * 72.5, y * 72.5)

                scene.add(power_up_object)


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

    teleporter = GameObjectConstants.Teleporter.TELEPORTER
    teleporter.transform.position = Vector2(2500, 4800)
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
