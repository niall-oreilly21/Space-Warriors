import json

from pygame import Vector2

from App.Constants.GameObjectConstants import GameObjectConstants
from Engine.GameObjects.Tiles.Tile import Tile
from Engine.GameObjects.Tiles.TileAttributes import TileAttributes
from Engine.GameObjects.Tiles.Tileset import Tileset


def map_load(scene):
    tileset = Tileset("Assets/SpriteSheets/Tilesets/plain_tileset2.png", 36, 36)

    # Add tiles to the tileset
    tileset.add_tile(Tile("Grass", 1, Vector2(216, 12)))
    tileset.add_tile(Tile("Water", 2, Vector2(264, 156)))
    tileset.add_tile(Tile("Dark Grass", 3, Vector2(216, 108)))
    tileset.add_tile(Tile("Dirt", 5, Vector2(306, 12)))
    tileset.add_tile(Tile("Sand", 6, Vector2(216, 156)))
    tileset.add_tile(Tile("Dirt", 7, Vector2(216, 156)))
    tileset.add_tile(Tile("CoarseDirt", 9, Vector2(216, 108)))

    map_data = []

    # load map data
    file_path = "Assets/SpriteSheets/Tilesets/PlanetA.json"

    with open(file_path, "r") as file:
        json_data = json.load(file)

    tile_data = json_data["grounds"]
    object_data = json_data["objects"]

    for x in range(100):
        row = []
        for z in range(100):
            tile = TileAttributes(2, False, None)
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
            if s_id == 2:
                map_data[y][x] = TileAttributes(s_id, True, c_value)
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
                tree_object = GameObjectConstants.TALL_TREE.clone()
                tree_object.transform.position = Vector2(x * 70, y * 70)  # starting area forces every tree to one point

                scene.add(tree_object)

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
