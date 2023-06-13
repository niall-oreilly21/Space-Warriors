import json
import random

from pygame import Vector2

from App.Components.Colliders.PlayerCollider import PlayerCollider
from App.Components.Controllers.BossEnemyController import BossEnemyController
from App.Components.Controllers.EnemyController import EnemyController
from App.Components.Controllers.EnemyHealthBarController import EnemyHealthBarController
from App.Components.Controllers.HealthBarController import HealthBarController
from App.Components.Controllers.PetController import PetController
from App.Components.Controllers.PlayerController import PlayerController
from App.Components.Controllers.ZapEnemyController import ZapEnemyController
from App.Constants.GameConstants import GameConstants
from App.Constants.EntityConstants import EntityConstants
from App.Constants.GameObjectConstants import GameObjectConstants
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.GameObjects.Components.Physics.WaypointFinder import WaypointFinder
from Engine.GameObjects.Gun.GunController import GunController
from Engine.GameObjects.Tiles.Tile import Tile
from Engine.GameObjects.Tiles.TileAttributes import TileAttributes
from Engine.GameObjects.Tiles.Tileset import Tileset
from Engine.Graphics.Materials.TextureMaterial2D import TextureMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Enums.GameObjectEnums import GameObjectCategory
from Engine.Other.Enums.RendererLayers import RendererLayers


class MapLoader:
    def __init__(self, player, player_health_bar, pet, ui_helper_texts):
        self.__player = player
        self.__player_health_bar = player_health_bar
        self.__player_health_bar.add_component(HealthBarController("Player Health Bar Controller", self.__player))
        self.__pet = pet
        self.__ui_helper_texts = ui_helper_texts
        self.__enemies = \
            {
                GameConstants.Scene.EARTH: [],
                GameConstants.Scene.MARS: [],
                GameConstants.Scene.SATURN: [],
                GameConstants.Scene.HOUSE: []
            }

        self.__load_player_components()
        self.__load_pet_components()

    def __load_player_components(self):
        self.__player.add_component(Rigidbody2D("Rigid"))
        player_box_collider = BoxCollider2D("Box")
        player_box_collider.scale = Vector2(1, 0.5)
        player_box_collider.offset = Vector2(0, 20)
        self.__player.add_component(player_box_collider)
        material_player = GameConstants.Player.MATERIAL_GIRL
        self.__player.add_component(SpriteRenderer2D("player", material_player, RendererLayers.Player))
        self.__player.add_component(SpriteAnimator2D("player", GameConstants.Player.PLAYER_ANIMATOR_INFO, material_player,
                                                     ActiveTake.PLAYER_IDLE_DOWN, GameConstants.CHARACTER_ANIMATOR_MOVE_SPEED))
        player_controller = PlayerController("Player movement", GameConstants.Player.MOVE_SPEED,
                                             GameConstants.Player.MOVE_SPEED, player_box_collider)
        self.__player.add_component(player_controller)
        player_collider = PlayerCollider("Players attack collider")
        self.__player.add_component(player_collider)

    def __load_pet_components(self):
        material_pet = GameConstants.PetDog.MATERIAL_PET
        self.__pet.add_component(SpriteRenderer2D("PetRenderer", material_pet, RendererLayers.Player))
        self.__pet.get_component(SpriteRenderer2D).flip_x = True
        self.__pet.add_component(SpriteAnimator2D("PetAnimator", GameConstants.PetDog.PET_ANIMATOR_INFO, material_pet,
                                                  ActiveTake.PET_DOG_SIT, GameConstants.CHARACTER_ANIMATOR_MOVE_SPEED))
        self.__pet.get_component(SpriteAnimator2D).is_infinite = True
        self.__pet.add_component(Rigidbody2D("PetRigidbody"))
        self.__pet.add_component(PetController("PetMovement", self.__player, 25))
        pet_collider = BoxCollider2D("PetCollider")
        pet_collider.scale = Vector2(2.5, 2.5)
        self.__pet.add_component(pet_collider)

    def map_load(self, scene, planet_json):
        tileset = Tileset("Assets/SpriteSheets/Tilesets/plain_tileset2.png", 36, 36)

        # Add tiles to the tileset
        tileset.add_tile(Tile("Grass", GameConstants.Tile.GRASS, Vector2(216, 12)))
        tileset.add_tile(Tile("Water", GameConstants.Tile.WATER, Vector2(264, 156)))
        tileset.add_tile(Tile("Dark Grass", GameConstants.Tile.WOOD, Vector2(216, 108)))
        tileset.add_tile(Tile("Dirt", GameConstants.Tile.DIRT, Vector2(308, 12)))
        tileset.add_tile(Tile("Sand", GameConstants.Tile.SAND, Vector2(216, 156)))
        tileset.add_tile(Tile("CoarseDirt", GameConstants.Tile.COARSE_DIRT, Vector2(216, 108)))
        tileset.add_tile(Tile("SaturnDirt", 10, Vector2(308, 12)))
        tileset.add_tile(Tile("SaturnSand", 7, Vector2(216, 156)))
        tileset.add_tile(Tile("SaturnSpawnRegion", 4, Vector2(216, 156)))
        tileset.add_tile(Tile("Wood", GameConstants.Tile.DARK_GRASS, Vector2(307,60)))

        map_data = []

        # load map data
        file_path = planet_json

        with open(file_path, "r") as file:
            json_data = json.load(file)

        tile_data = json_data["grounds"]
        object_data = json_data["objects"]

        width = 110
        height = 120

        if scene.name == GameConstants.Scene.EARTH:
            self.__load_planet_earth_specifics(scene)
            self.__color_tiles(map_data, tile_data, width, height, None, None)
        elif scene.name == GameConstants.Scene.MARS:
            self.__load_planet_mars_specifics(scene)
            self.__color_tiles(map_data, tile_data, width, height, [255, 100, 150], 220)
        elif scene.name == GameConstants.Scene.SATURN:
            self.__load_planet_saturn_specifics(scene)
            self.__color_tiles(map_data, tile_data, width, height, [255, 255, 0], 150)
        elif scene.name == GameConstants.Scene.HOUSE:
            self.__load_house_specifics(scene)
            self.__color_tiles(map_data, tile_data, 15, 10, [255, 255, 255], 255)

        # Object generation
        for object in object_data:
            if object["x"] < width and object["y"] < height:
                x = object["x"]
                y = object["y"]
                id = object["t"]["id"]
                if id == 5:
                    if scene.name is GameConstants.Scene.EARTH:
                        tree_object = random.choice(
                            [GameObjectConstants.Foliage.TALL_TREE.clone(),
                             GameObjectConstants.Foliage.LOW_TREE.clone()])
                        tree_collider = BoxCollider2D("TreeCollider")
                        if tree_object.name == "Tree":
                            tree_collider.scale = Vector2(0.3, 0.15)
                            tree_collider.offset = Vector2(3, 72)
                        else:
                            tree_collider.scale = Vector2(0.5, 0.25)
                            tree_collider.offset = Vector2(0, 32)
                        tree_object.add_component(tree_collider)
                        tree_object.transform.position = Vector2(x * 71,
                                                                 y * 71)  # starting area forces every tree to one point
                        scene.add(tree_object)
                    elif scene.name is GameConstants.Scene.SATURN:
                        tree_object = GameObjectConstants.NaturalStructures.ROCK_THREE.clone()
                        tree_collider = BoxCollider2D("TreeCollider")
                        tree_object.add_component(tree_collider)
                        tree_object.transform.position = Vector2(x * 71,
                                                                 y * 71)  # starting area forces every tree to one point
                        scene.add(tree_object)
                elif id == 15:
                    if scene.name is GameConstants.Scene.EARTH:
                        bush_object = random.choice(
                            [GameObjectConstants.Foliage.BUSH_ONE.clone(), GameObjectConstants.Foliage.BUSH_TWO.clone(),
                             GameObjectConstants.Foliage.BUSH_FOUR.clone(),
                             GameObjectConstants.NaturalStructures.ROCK_ONE.clone()])
                        bush_object.add_component(BoxCollider2D("BushCollider"))
                        if bush_object.name == "RockOne":
                            scale = random.uniform(0.7, 2)
                            bush_object.transform.scale = Vector2(scale, scale)
                        bush_object.transform.position = Vector2(x * 72, y * 72)
                        scene.add(bush_object)
                    elif scene.name is GameConstants.Scene.MARS:
                        bush_object = random.choice([GameObjectConstants.Foliage.BUSH_THREE.clone(),
                                                     GameObjectConstants.Foliage.DEAD_BUSH.clone()])
                        bush_object.add_component(BoxCollider2D("BushCollider"))
                        bush_object.transform.position = Vector2(x * 72, y * 72)
                        scene.add(bush_object)
                    elif scene.name is GameConstants.Scene.SATURN:
                        bush_object = GameObjectConstants.Foliage.DEAD_BUSH.clone()
                        bush_object.add_component(BoxCollider2D("BushCollider"))
                        bush_object.transform.position = Vector2(x * 72, y * 72)
                        scene.add(bush_object)
                elif id == 11:
                    lilypad_object = random.choice([GameObjectConstants.Foliage.LILYPAD_ONE.clone(),
                                                    GameObjectConstants.Foliage.LILYPAD_TWO.clone()])
                    lilypad_object.transform.rotation = random.randint(0, 360)
                    lilypad_object.transform.position = Vector2(x * 72.5, y * 72.5)

                    scene.add(lilypad_object)
                elif id == 1:
                    if scene.name is GameConstants.Scene.EARTH:
                        power_up_object = random.choice([GameObjectConstants.Consumables.SPEED_POWER_UP.clone(),
                                                         GameObjectConstants.Consumables.HEAL_POWER_UP.clone(),
                                                         GameObjectConstants.Consumables.ATTACK_POWER_UP.clone(),
                                                         GameObjectConstants.Consumables.DEFENSE_POWER_UP.clone(),
                                                         GameObjectConstants.Consumables.RANDOM_POWER_UP.clone()])
                    elif scene.name is GameConstants.Scene.MARS:
                        power_up_object = random.choice([GameObjectConstants.Consumables.SPEED_POWER_UP.clone(),
                                                         GameObjectConstants.Consumables.HEAL_POWER_UP.clone(),
                                                         GameObjectConstants.Consumables.ATTACK_POWER_UP.clone(),
                                                         GameObjectConstants.Consumables.DEFENSE_POWER_UP.clone(),
                                                         GameObjectConstants.Consumables.RANDOM_POWER_UP.clone(),
                                                         GameObjectConstants.Consumables.NIGHT_VISION_POWER_UP.clone(),
                                                         GameObjectConstants.Consumables.NIGHT_VISION_POWER_UP.clone()])
                    else:
                        power_up_object = random.choice([GameObjectConstants.Consumables.SPEED_POWER_UP.clone(),
                                                         GameObjectConstants.Consumables.HEAL_POWER_UP.clone(),
                                                         GameObjectConstants.Consumables.HEAL_POWER_UP.clone(),
                                                         GameObjectConstants.Consumables.HEAL_POWER_UP.clone(),
                                                         GameObjectConstants.Consumables.ATTACK_POWER_UP.clone(),
                                                         GameObjectConstants.Consumables.DEFENSE_POWER_UP.clone(),
                                                         GameObjectConstants.Consumables.RANDOM_POWER_UP.clone()])
                    power_up_object.transform.position = Vector2(x * 72.5, y * 72.5)
                    power_up_collider = BoxCollider2D("PowerUpCollider")
                    power_up_collider.scale = Vector2(2.5, 2.5)
                    power_up_object.add_component(power_up_collider)
                    scene.add(power_up_object)

        # Create the map using the tileset and map data
        map_tiles = tileset.create_map(map_data)

        for tiles in map_tiles:
            for tile in tiles:
                tile.transform.scale = Vector2(2, 2)
                tile.transform.position *= 2
                scene.add(tile)

    def __color_tiles(self, map_data, tile_data, width, height, color, alpha):
        # Create Default Tiles
        for x in range(height):
            row = []
            for z in range(width):
                tile = TileAttributes(GameConstants.Tile.WATER, False, color, alpha)
                row.append(tile)
            map_data.append(row)

        for ground in tile_data:
            if ground["x"] < width and ground["y"] < height:
                x = ground["x"]
                y = ground["y"]
                s_id = ground["s"]["id"]
                if s_id == GameConstants.Tile.WATER:
                    map_data[y][x] = TileAttributes(s_id, True, color, alpha)
                elif s_id == 8:
                    map_data[y][x] = TileAttributes(GameConstants.Tile.WOOD, True, (0, 0, 0), 255)
                else:
                    map_data[y][x] = TileAttributes(s_id, False, color, alpha)

    def load_planet_dynamic_objects(self, scene):
        if not scene.contains(self.__player):
            scene.add(self.__player)
            scene.add(self.__player_health_bar)

        if not scene.contains(self.__pet):
            if self.__pet.get_component(PetController).adopted:
                scene.add(self.__pet)

        self.__check_enemy_in_scene(scene)
        scene.start()
        return len(self.__enemies[scene.name])

    def __check_enemy_in_scene(self, scene):
        if self.__enemies[scene.name] is not None:
            for enemy in self.__enemies[scene.name]:
                enemy.health_bar.get_component(EnemyHealthBarController).reset_health_bar_visibility()

                if not scene.contains(enemy):
                    scene.add(enemy)
        else:
            print(scene.name)
    def __add_enemy_health_bar_to_scene(self, enemy, enemy_health_bar_texture, scene):
        health_bar = GameObjectConstants.HealthBar.ENEMY_HEALTH_BAR.clone()
        self.__set_texture_for_enemy_health_bar(health_bar, enemy_health_bar_texture)
        health_bar.add_component(EnemyHealthBarController("Health Bar Controller Enemy", enemy))
        enemy.health_bar = health_bar
        scene.add(health_bar)

    def __set_texture_for_enemy_health_bar(self, health_bar, enemy_health_bar_texture):
        for renderer in health_bar.get_components(Renderer2D):
            if isinstance(renderer.material, TextureMaterial2D):
                renderer.material.texture = enemy_health_bar_texture

    def __add_enemy_to_scene(self, enemy, enemy_health_bar_texture, scene):
        self.__enemies[scene.name].append(enemy)
        self.__add_enemy_health_bar_to_scene(enemy,enemy_health_bar_texture, scene)
        scene.add(enemy)

    def load_planet_earth_enemies(self, scene):
        enemy = EntityConstants.Enemy.RAT_ENEMY.clone()
        enemy.add_component(EnemyController("Enemy movement", self.__player, GameConstants.EnemyRat.MOVE_SPEED, 400))

        self.load_enemies(EntityConstants.Enemy.ENEMY_WAYPOINTS, GameObjectCategory.Rat, enemy, scene)

    def load_planet_mars_enemies(self, scene):
        enemy = EntityConstants.Enemy.WOLF_ENEMY.clone()
        enemy.add_component(ZapEnemyController("Enemy movement", self.__player, GameConstants.EnemyWolf.MOVE_SPEED, 600, 20, 4))

        self.load_enemies(EntityConstants.Enemy.ENEMY_WAYPOINTS, GameObjectCategory.Wolf, enemy, scene)

    def load_planet_saturn_enemies(self, scene):
        gun = GameObjectConstants.Gun.Gun

        enemy = EntityConstants.Enemy.ALIEN_ENEMY.clone()
        enemy.add_component(BossEnemyController("Enemy movement", self.__player, GameConstants.EnemyAlien.MOVE_SPEED, 800, 10, gun))

        gun.add_component(GunController("Enemy Gun Controller", enemy))
        scene.add(gun)

        self.load_enemies(EntityConstants.Enemy.ENEMY_WAYPOINTS, GameObjectCategory.Alien, enemy, scene)

        # Boss?
        init_pos = 3200, 4000
        boss = EntityConstants.Enemy.ALIEN_ENEMY
        boss.initial_position = Vector2(init_pos)
        boss.transform.scale = Vector2(5, 5)
        boss.transform.position = Vector2(3207.8, 4013)
        boss.add_component(
            BossEnemyController("Enemy movement", self.__player, GameConstants.EnemyAlien.MOVE_SPEED, 800, 10, gun))
        boss.get_component(WaypointFinder).waypoints = [Vector2(init_pos), Vector2(3000, 4000)]

    def __load_planet_earth_specifics(self, scene):
        ruin = GameObjectConstants.UnnaturalStructures.RUIN_ONE.clone()
        ruin.transform.position = Vector2(2050, 2600)
        scene.add(ruin)

        house = GameObjectConstants.UnnaturalStructures.HOUSE.clone()
        house.transform.position = Vector2(2700, 2400)
        house.transform.scale = Vector2(0.6,0.6)
        scene.add(house)

        ruin = GameObjectConstants.UnnaturalStructures.RUIN_TWO.clone()
        ruin.transform.position = Vector2(4200, 1900)
        ruin.transform.scale = Vector2(3, 3)
        scene.add(ruin)

        ruin = GameObjectConstants.UnnaturalStructures.RUIN_THREE.clone()
        ruin.transform.position = Vector2(3100, 4600)
        scene.add(ruin)

        statue = GameObjectConstants.UnnaturalStructures.STATUE.clone()
        statue.transform.position = Vector2(2800, 4700)
        scene.add(statue)

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

        scene.add(self.__pet)
        self.__load_teleporter(scene, Vector2(584, 6350.2))
        self.__load_ui_texts(scene)

    def __load_planet_mars_specifics(self, scene):
        ruin = GameObjectConstants.UnnaturalStructures.RUIN_FOUR.clone()
        ruin.transform.position = Vector2(2450, 3500)
        scene.add(ruin)

        ruin = GameObjectConstants.UnnaturalStructures.RUIN_FIVE.clone()
        ruin.transform.position = Vector2(3700, 3700)
        scene.add(ruin)

        ruin = GameObjectConstants.UnnaturalStructures.RUIN_SIX.clone()
        ruin.transform.position = Vector2(3900, 1800)
        scene.add(ruin)

        statue = GameObjectConstants.UnnaturalStructures.STATUE.clone()
        statue.transform.position = Vector2(2500, 4700)
        scene.add(statue)

        self.__load_teleporter(scene, Vector2(3640, 4700))
        self.__load_ui_texts(scene)

    def __load_planet_saturn_specifics(self, scene):
        ruin = GameObjectConstants.UnnaturalStructures.RUIN_SEVEN.clone()
        ruin.transform.position = Vector2(2800, 3500)
        ruin.transform.scale = Vector2(3, 3)
        scene.add(ruin)

        ruin = GameObjectConstants.UnnaturalStructures.RUIN_EIGHT.clone()
        ruin.transform.position = Vector2(3700, 2600)
        ruin.transform.scale = Vector2(3, 3)
        scene.add(ruin)

        ruin = GameObjectConstants.UnnaturalStructures.RUIN_NINE.clone()
        ruin.transform.position = Vector2(4500, 3500)
        ruin.transform.scale = Vector2(3, 3)
        scene.add(ruin)

        self.__load_teleporter(scene, Vector2(3640, 4700))
        self.__load_ui_texts(scene)

    def __load_house_specifics(self, scene):

        enemy = EntityConstants.Enemy.RAT_ENEMY.clone()
        enemy.initial_position = Vector2(0, 0)
        enemy.add_component(
            EnemyController("Enemy movement", self.__player, GameConstants.EnemyRat.MOVE_SPEED, 600))

        door = GameObjectConstants.UnnaturalStructures.DOOR.clone()
        door.transform.position = Vector2(471, 580)
        door.transform.scale = Vector2(.4, .4)
        scene.add(door)

        bed = GameObjectConstants.UnnaturalStructures.BED.clone()
        bed.transform.position = Vector2(322, 72)
        bed.transform.scale = Vector2(.2,.2)
        scene.add(bed)

        table = GameObjectConstants.UnnaturalStructures.TABLE.clone()
        table.transform.position = Vector2(247, 282)
        table.transform.scale = Vector2(.3,.3)
        scene.add(table)

        couch = GameObjectConstants.UnnaturalStructures.COUCH.clone()
        couch.transform.position = Vector2(814, 342)
        couch.transform.scale = Vector2(.4, .4)
        couch.transform.rotation = -90
        scene.add(couch)

        window = GameObjectConstants.UnnaturalStructures.WINDOW.clone()
        window.transform.position = Vector2(122, 12)
        window.transform.scale = Vector2(.5,.5)
        scene.add(window)

        window = GameObjectConstants.UnnaturalStructures.WINDOW.clone()
        window.transform.position = Vector2(650, 12)
        window.transform.scale = Vector2(.5,.5)
        scene.add(window)

        window = GameObjectConstants.UnnaturalStructures.WINDOW.clone()
        window.transform.position = Vector2(1000, 142)
        window.transform.scale = Vector2(.5, .5)
        window.transform.rotation = -90
        scene.add(window)

        self.load_enemies(EntityConstants.Enemy.ENEMY_WAYPOINTS, GameObjectCategory.Rat, enemy, scene)

    def __load_teleporter(self, scene, position):
        teleporter = GameObjectConstants.Teleporter.TELEPORTER.clone()
        teleporter.transform.position = position
        scene.add(teleporter)

    def __load_ui_texts(self, scene):
        for ui_helper_text in self.__ui_helper_texts:
            scene.add(ui_helper_text)

    def load_enemies(self, enemy_waypoints, enemy_type, enemy, scene):
        enemy_type_name = EntityConstants.Enemy.ALIEN_ENEMY_NAME
        enemy_health_bar_texture = GameObjectConstants.HealthBar.ALIEN_ENEMY_HEALTH_BAR_IMAGE
        if enemy_type == GameObjectCategory.Rat:
            if scene.name == GameConstants.Scene.HOUSE:
                enemy_type_name = EntityConstants.Enemy.HOUSE_RAT_ENEMY_NAME
            else:
                enemy_type_name = EntityConstants.Enemy.RAT_ENEMY_NAME
            enemy_health_bar_texture = GameObjectConstants.HealthBar.RAT_ENEMY_HEALTH_BAR_IMAGE
        elif enemy_type == GameObjectCategory.Wolf:
            enemy_type_name = EntityConstants.Enemy.WOLF_ENEMY_NAME
            enemy_health_bar_texture = GameObjectConstants.HealthBar.WOLF_ENEMY_HEALTH_BAR_IMAGE

        for waypoints in enemy_waypoints[enemy_type_name]:
            new_enemy = enemy.clone()
            new_enemy.initial_position = waypoints[0]
            new_enemy.get_component(WaypointFinder).waypoints = waypoints
            self.__add_enemy_to_scene(new_enemy,enemy_health_bar_texture, scene)
