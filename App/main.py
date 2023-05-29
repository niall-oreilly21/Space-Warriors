import json
import os
import random

import pygame
from pygame import Vector2, Rect

from App.Components.Colliders.PlayerAttackCollider import PlayerAttackCollider
import App.Constants.GameObjects
from App.Constants import GameObjects
from Engine.GameObjects.Character import Character
from Engine.GameObjects.Components.Cameras.ThirdPersonController import ThirdPersonController
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Cameras.Camera import Camera
from Engine.GameObjects.Tiles.Tile import Tile
from Engine.GameObjects.Tiles.TileAttributes import TileAttributes
from Engine.GameObjects.Tiles.Tileset import Tileset
from Engine.Managers.CollisionManager import CollisionManager
from Engine.GameObjects.GameObject import GameObjectType, GameObjectCategory, GameObject
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Sprites.Take import Take
from Engine.Managers.CameraManager import CameraManager
from Engine.Managers.EventSystem.EventDispatcher import EventDispatcher
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Interfaces.IStartable import IStartable
from Engine.Time.GameTime import GameTime
from App.Components.PlayerController import PlayerController
from Engine.Managers.RendererManager import RendererManager
from Engine.Managers.Scene import Scene
from Engine.Managers.SceneManager import SceneManager
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Materials.TextMaterial2D import TextMaterial2D
from Engine.Graphics.Materials.TextureMaterial2D import TextureMaterial2D
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Other.Transform2D import Transform2D
from App.Constants.Constants import Constants

def print_array_size(arr):
    num_rows = len(arr)
    num_cols = len(arr[0]) if arr else 0

    print("Number of rows:", num_rows)
    print("Number of columns:", num_cols)

def update(game_time):
    scene.update(game_time)

# Initialize Pygame
pygame.init()

# Set up the display window
screen_width = 1
screen_height = 1

# # Create the display window
screen_info = pygame.display.Info()
screen_resolution = Vector2(screen_info.current_w, screen_info.current_h)


# Set the environment variable to center the window
os.environ['SDL_VIDEO_CENTERED'] = '1'

screen = pygame.display.set_mode((500, 500))

cameraGameObject = GameObject("MainCamera", Transform2D(Vector2(0, 0), Vector2(0, 0), Vector2(0, 0)), GameObjectType.Dynamic, GameObjectCategory.Player)
camera = Camera("MainCamera", 1000, 500)
cameraGameObject.add_component(camera)
managers = []


sceneManager = SceneManager(EventDispatcher())

cameraManager = CameraManager(screen, sceneManager, None)
cameraManager.add(cameraGameObject)

cameraManager.set_active_camera("MainCamera")

# Create a font object
font = pygame.font.Font(None, 80)

font_name = None


text_material = TextMaterial2D(font, font_name, "Hello, World!", Vector2(150,40), (255, 0, 0))
sprite_transform = Transform2D(Vector2(10, 100), 0, Vector2(1, 1))

starting_area = Vector2(2050, 5300)

scene = Scene("New Scene")
player = Character("Player", Constants.Player.DEFAULT_HEALTH, Constants.Player.DEFAULT_ATTACK_DAMAGE, 2,
                   Constants.Player.TOTAL_LIVES, Transform2D(starting_area, 0, Vector2(1, 1)),
                   GameObjectType.Dynamic, GameObjectCategory.Player)
player.add_component(Rigidbody2D("Rigid"))
player_box_collider = BoxCollider2D("Box")
player.add_component(player_box_collider)
material_player = Constants.Player.MATERIAL_GIRL
player.add_component(SpriteRenderer2D("player", material_player, 10))
player.add_component(SpriteAnimator2D("player", Constants.Player.PLAYER_ANIMATOR_INFO, material_player,
                                      ActiveTake.PLAYER_IDLE_DOWN, Constants.CHARACTER_MOVE_SPEED))
player_controller = PlayerController("Player movement", 0.3, 0.3, player_box_collider)
player.add_component(player_controller)
player_collider = PlayerAttackCollider("Players attack collider")
player.add_component(player_collider)



enemy = Character("Enemy", 200, Transform2D(Vector2(200, 500), 0, Vector2(1, 1)), GameObjectType.Dynamic, GameObjectCategory.Player)
enemy.add_component(BoxCollider2D("Box-1"))


text = GameObject("Text", Transform2D(Vector2(0, 0),0, Vector2(1, 1)), GameObjectType.Dynamic, GameObjectCategory.Player)

image = pygame.image.load("menu_button.png")
texture_material = TextureMaterial2D(image, None, Vector2(0, 0), None)
text.add_component(Renderer2D("Renderer-2", texture_material, 1))
text.add_component(Renderer2D("Renderer-1", text_material, 2))

#text.add_component(BoxCollider2D("Box-2"))

scene.add(player)
scene.add(enemy)
#scene.add(text)

# Load an image and create a TextureMaterial2D object with it
image = pygame.image.load("image.png")
material = TextureMaterial2D(image, None, Vector2(0, 0), 60, None)

material2 = TextureMaterial2D(image, (255,255,0), Vector2(0, 0), None)

enemy.add_component(SpriteRenderer2D("renderer-enemy", material2, 3))


sceneManager.add("Game", scene)
sceneManager.set_active_scene("Game")
renderManager = RendererManager(screen, sceneManager, cameraManager)

frame_rects = []

rect = pygame.Rect(234, 120, 60, 72)
frame_rects.append(rect)
rect = pygame.Rect(342, 120, 60, 72)
frame_rects.append(rect)

frame_rects2 = []

rect = pygame.Rect(18, 6, 60, 90)
frame_rects2.append(rect)
rect = pygame.Rect(126, 6, 60, 90)
frame_rects2.append(rect)

frame_rects3 = [Rect(6, 114, 84, 84)]

animator_info = [Take(ActiveTake.PLAYER_RUNNING, frame_rects), Take(ActiveTake.PLAYER_WALKING, frame_rects2), Take(ActiveTake.COOK, frame_rects3)]

animator = SpriteAnimator2D("animator", animator_info, material, ActiveTake.COOK, 5)
renderer = SpriteRenderer2D("renderer", material, 4)
player.add_component(renderer)

playerController = PlayerController("Player movement", 0.3, 0.3, EventDispatcher())
player.add_component(playerController)
#player.add_component(EnemyCollider("Collider"))

animator1 = SpriteAnimator2D("animator-enemy", animator_info, material2, ActiveTake.COOK, 5)
enemy.add_component(animator1)

player.add_component(animator)

managers.append(cameraManager)
managers.append(sceneManager)

#enemy2 = player.clone()



# scene.add(enemy2)
# scene.remove(player)
#
# print(enemy2.get_component(Renderer2D))

game_time = GameTime()
cameraGameObject.add_component(ThirdPersonController("Third Person Controller", player))

collider_system = CollisionManager(200, sceneManager, cameraManager)
managers.append(collider_system)



renderManager.is_debug_mode = True

#for i in range(200):
# newEnemy = enemy.clone()
# scene.add(newEnemy)
# newEnemy.transform.translate_by(Vector2(random.randint(-4000, 8000), random.randint(-1000, 1000)))

for manager in managers:
    if isinstance(manager, IStartable):
        manager.start()




tileset = Tileset("Assets/SpriteSheets/Tilesets/plain_tileset2.png", 36, 36)

# Add tiles to the tileset
tileset.add_tile(Tile("Grass", 1, Vector2(216, 12)))
tileset.add_tile(Tile("Water", 2, Vector2(264, 156)))
tileset.add_tile(Tile("Dark Grass", 3, Vector2(216, 108)))
tileset.add_tile(Tile("Dirt", 5, Vector2(216, 156)))
tileset.add_tile(Tile("Sand", 6, Vector2(216, 156)))
tileset.add_tile(Tile("Dirt", 7, Vector2(216, 156)))
tileset.add_tile(Tile("CoarseDirt", 9, Vector2(216, 108)))



# Add more tiles as needed

# Define map data
# map_data = [
#     [TileAttributes(1, False, None), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)],
#     [TileAttributes(1, False, None), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)],
#     [TileAttributes(1, False, None), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)],
# [TileAttributes(1, False, None), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)],
#     [TileAttributes(1, False, None), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)],
# [TileAttributes(1, False, None), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)],
#     [TileAttributes(1, False, None), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)],
#     [TileAttributes(1, False, None, 10), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)],
# [TileAttributes(1, False, None, 10), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)],
#     [TileAttributes(1, False, None, 10), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)],
#     [TileAttributes(1, False, None, 10), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)],
# [TileAttributes(1, False, None, 10), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)],
#     [TileAttributes(1, False, None, 10), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)],
#     [TileAttributes(1, False, None, 10), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)],
# [TileAttributes(1, False, None, 10), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)],
#     [TileAttributes(1, False, None, 10), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)],
#     [TileAttributes(1, False, None, 10), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)],
# [TileAttributes(1, False, None, 10), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)],
#     [TileAttributes(1, False, None, 10), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)],
#     [TileAttributes(1, False, None, 10), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)]
#
#
#     # More map data rows
# ]

    # map_data.append([TileAttributes(1, True, None), TileAttributes(1, False), TileAttributes(1, False, None), TileAttributes(1, False)])
#
# for row in map_data:
#     for i in range(5):
#         row.append(TileAttributes(1, False))

# Define the number of times to repeat the appending process

num_repeats = 100

# Create the map_data using a nested list comprehension
#map_data = [[TileAttributes(1, False, None) for _ in range(num_repeats)] for _ in range(num_repeats)]
map_data = []




#load map data
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
# for object in object_data:
#     if object["x"] < 100 and object["y"] < 100:
#         x = object["x"]
#         y = object["y"]
#         c_value = object["c"]
#         id = object["t"]["id"]
#         if id == 5:
#             tree_object = GameObjects.GameObjects.TALL_TREE.clone()
#             tree_object.transform.position = Vector2(x*70,y*70) #starting area forces every tree to one point
#             print(tree_object.transform.position)
#
#             scene.add(tree_object)

ruin = GameObjects.GameObjects.RUIN_ONE.clone()
ruin.transform.position = Vector2(2000,5000)
scene.add(ruin)

ruin = GameObjects.GameObjects.RUIN_TWO.clone()
ruin.transform.position = Vector2(1800,5000)
scene.add(ruin)

boulder = GameObjects.GameObjects.BOULDER_TWO.clone()
boulder.transform.position = Vector2(2200,5000)
scene.add(boulder)

statue = GameObjects.GameObjects.STATUE.clone()
statue.transform.position = Vector2(2000,5400)
scene.add(statue)



# # Add the modified tree objects back to the scene
# for tree_object in tree_objects:
#     scene.add(tree_object)

# tree_object = GameObjects.GameObjects.TALL_TREE.clone()
# tree_object2 = GameObjects.GameObjects.TALL_TREE.clone()
#
# tree_object.transform.position = Vector2(2300,5000) #starting area forces every tree to one point
# scene.add(tree_object)
#
# tree_object2.transform.position = Vector2(2350,5000) #starting area forces every tree to one point
# scene.add(tree_object2)


# Create the map using the tileset and map data
map_tiles = tileset.create_map(map_data)



# # Create the map using the tileset and map data
# map_tiles = tileset.create_map(map_data)

print_array_size(map_tiles)


for tiles in map_tiles:
    for tile in tiles:
        tile.transform.scale = Vector2(2,2)
        tile.transform.position *= 2
        # random_translation = Vector2(random.randint(1000, 2000), random.randint(10, 10))
        # tile.transform.translate_by(random_translation)
        scene.add(tile)

        if tile.get_component(BoxCollider2D):
            tile.get_component(BoxCollider2D).start()

colliders = scene.get_all_components_by_type(BoxCollider2D)

# Fill the screen with a background color
background_color = (0, 0, 0) # white
if screen is  not None:
    screen.fill(background_color)
# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game_time.tick()

    for manager in managers:
        manager.update(game_time)

    if screen is not None:
        screen.fill(background_color)

    # for tiles in map_tiles:
    #     for tile in tiles:
    #         if tile.get_component(BoxCollider2D):
    #             tile.get_component(BoxCollider2D).draw(screen , cameraManager)
    #
    # player.get_component(BoxCollider2D).draw(screen, cameraManager)
    # enemy.get_component(BoxCollider2D).draw(screen, cameraManager)
    #enemy2.get_component(BoxCollider2D).draw(screen, cameraManager)
    # text.get_component(BoxCollider2D).draw(screen, cameraManager)


    renderManager.draw(game_time)


    pygame.display.update()
    game_time.limit_fps(60)

pygame.quit()








