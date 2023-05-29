import os
import pygame
from pygame import Vector2, Rect

from App.Components.Colliders.AttackBoxCollider2D import AttackBoxCollider2D
from App.Components.Colliders.PlayerAttackCollider2D import PlayerAttackCollider
from App.Components.Controllers.EnemyController import EnemyController
from App.Constants.Constants import Constants
from Engine.GameObjects.Character import Character
from Engine.Graphics.Sprites.Take import Take
from Engine.Managers.CollisionManager import CollisionManager
from Engine.GameObjects.Components.Cameras.ThirdPersonController import ThirdPersonController
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Cameras.Camera import Camera
from Engine.GameObjects.GameObject import GameObjectType, GameObjectCategory, GameObject
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Managers.CameraManager import CameraManager
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Interfaces.IStartable import IStartable
from Engine.Time.GameTime import GameTime
from App.Components.Controllers.PlayerController import PlayerController
from Engine.Managers.RendererManager import RendererManager
from Engine.Managers.Scene import Scene
from Engine.Managers.SceneManager import SceneManager
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Materials.TextMaterial2D import TextMaterial2D
from Engine.Graphics.Materials.TextureMaterial2D import TextureMaterial2D
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Other.Transform2D import Transform2D


def initialise_menu(background_material, title_text, menu_button_text_top, menu_button_text_bottom):
    camera_manager.set_active_camera("MenuCamera")

    menu_scene = Scene("MenuScene")
    menu_scene.add(camera_main_menu_game_object)
    scene_manager.add("MenuScene", menu_scene)
    scene_manager.set_active_scene("MenuScene")

    background = GameObject("MenuBackground", Transform2D(Vector2(0, 0), 0, Vector2(1, 1)))
    background.add_component(Renderer2D("MenuRenderer", background_material))

    title = GameObject("MenuTitle", Transform2D(Vector2(0, 0), 0, Vector2(1, 1)), GameObjectType.Static,
                       GameObjectCategory.Menu)
    title_font = pygame.font.Font(Constants.Menu.TITLE_FONT_PATH, Constants.Menu.TITLE_FONT_SIZE)
    title_text_material = TextMaterial2D(title_font, Constants.Menu.TITLE_FONT_PATH, title_text,
                                         Vector2(Constants.VIEWPORT_WIDTH / 2, 120), (255, 255, 255))
    title.add_component(Renderer2D("TitleRenderer", title_text_material, 1))

    start_button = GameObject("StartButton",
                              Transform2D(Vector2(Constants.VIEWPORT_WIDTH / 2 - 150, 220), 0, Vector2(1, 1)),
                              GameObjectType.Static, GameObjectCategory.Menu)
    start_button_texture_material = TextureMaterial2D(Constants.Menu.MENU_BUTTON_IMAGE, None,
                                                      Vector2(0, 0), None)
    text_font = pygame.font.Font(Constants.Menu.TEXT_FONT_PATH, Constants.Menu.TEXT_FONT_SIZE)
    start_button_text_material = TextMaterial2D(text_font, Constants.Menu.TEXT_FONT_PATH, menu_button_text_top,
                                                Vector2(150, 27), (0, 0, 0))
    start_button.add_component(Renderer2D("StartButtonRenderer", start_button_texture_material, 1))
    start_button.add_component(Renderer2D("StartButtonTextRenderer", start_button_text_material, 2))

    end_button = start_button.clone()
    end_button.transform.position.y = 320
    renderers = end_button.get_components(Renderer2D)

    for renderer in renderers:
        if isinstance(renderer.material, TextMaterial2D):
            renderer.material.text = menu_button_text_bottom

    menu_scene.add(background)
    menu_scene.add(title)
    menu_scene.add(start_button)
    menu_scene.add(end_button)


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

screen = pygame.display.set_mode((400, 400))

camera_game_object = GameObject("MainCamera", Transform2D(Vector2(0, 0), Vector2(0, 0), Vector2(0, 0)),
                                GameObjectType.Dynamic, GameObjectCategory.Player)
camera = Camera("MainCamera", Constants.VIEWPORT_WIDTH, Constants.VIEWPORT_HEIGHT)

camera_game_object.add_component(camera)
managers = []
scene_manager = SceneManager()

camera_manager = CameraManager(screen, scene_manager)
camera_manager.add(camera_game_object)

camera_manager.set_active_camera("MainCamera")

# Create a font object
font_path = "Assets/Fonts/Starjedi.ttf"
font = pygame.font.Font(font_path, 80)
font_name = font_path

text_material = TextMaterial2D(font, font_name, "Hello, World!", Vector2(150, 40), (255, 0, 0))
sprite_transform = Transform2D(Vector2(10, 100), 0, Vector2(1, 1))

scene = Scene("New Scene")
player = Character("Player", Constants.Player.DEFAULT_HEALTH, Constants.Player.DEFAULT_ATTACK_DAMAGE, 2,
                   Constants.Player.TOTAL_LIVES, Transform2D(Vector2(300, 300), 0, Vector2(1, 1)),
                   GameObjectType.Dynamic, GameObjectCategory.Player)
player.add_component(Rigidbody2D("Rigid"))
player_box_collider = BoxCollider2D("Box")
player.add_component(player_box_collider)
material_player = Constants.Player.MATERIAL_GIRL
player.add_component(SpriteRenderer2D("player", material_player, 5))
player.add_component(SpriteAnimator2D("player", Constants.Player.PLAYER_ANIMATOR_INFO, material_player,
                                      ActiveTake.PLAYER_IDLE_DOWN, Constants.CHARACTER_MOVE_SPEED))
player_controller = PlayerController("Player movement", 0.3, 0.3, player_box_collider)
player.add_component(player_controller)
player_collider = PlayerAttackCollider("Players attack collider")
player.add_component(player_collider)

enemy = Character("Enemy", 70, 1, 1, 1, Transform2D(Vector2(0, 0), 0, Vector2(1.5, 1.5)), GameObjectType.Dynamic,
                  GameObjectCategory.Rat)
enemy.add_component(BoxCollider2D("Box-1"))
# enemy.add_component(Rigidbody2D("Rigid"))
material_enemy = Constants.EnemyRat.MATERIAL_ENEMY1
enemy.add_component(SpriteRenderer2D("enemy", material_enemy, 0))
enemy.add_component(SpriteAnimator2D("enemy", Constants.EnemyRat.ENEMY_ANIMATOR_INFO, material_enemy,
                                     ActiveTake.ENEMY_RAT_MOVE_DOWN, Constants.CHARACTER_MOVE_SPEED))
enemy_controller = EnemyController("Enemy movement", player, Constants.EnemyRat.MOVE_SPEED)
enemy.add_component(enemy_controller)

enemy2 = Character("Enemy2", 50, 2, 1, 1, Transform2D(Vector2(-1000, -1000), 0, Vector2(1.5, 1.5)),
                   GameObjectType.Dynamic,
                   GameObjectCategory.Wolf)
enemy2.add_component(BoxCollider2D("Box-3"))
# enemy.add_component(Rigidbody2D("Rigid"))
material_enemy = Constants.EnemyWolf.MATERIAL_ENEMY1
enemy2.add_component(SpriteRenderer2D("enemy2", material_enemy, 1))
enemy2.add_component(SpriteAnimator2D("enemy2", Constants.EnemyWolf.ENEMY_ANIMATOR_INFO, material_enemy,
                                      ActiveTake.ENEMY_WOLF_MOVE_DOWN, Constants.CHARACTER_MOVE_SPEED))
enemy_controller2 = EnemyController("Enemy movement 2", player, Constants.EnemyWolf.MOVE_SPEED)
enemy2.add_component(enemy_controller2)

enemy3 = Character("Enemy3", 50, 2, 1, 1, Transform2D(Vector2(1000, -1000), 0, Vector2(1.5, 1.5)),
                   GameObjectType.Dynamic,
                   GameObjectCategory.Wolf)
enemy3.add_component(BoxCollider2D("Box-3"))
# enemy.add_component(Rigidbody2D("Rigid"))
material_enemy = Constants.EnemyWolf.MATERIAL_ENEMY3
enemy3.add_component(SpriteRenderer2D("enemy2", material_enemy, 1))
enemy3.add_component(SpriteAnimator2D("enemy2", Constants.EnemyWolf.ENEMY_ANIMATOR_INFO, material_enemy,
                                      ActiveTake.ENEMY_WOLF_MOVE_DOWN, Constants.CHARACTER_MOVE_SPEED))
enemy_controller2 = EnemyController("Enemy movement 2", player, Constants.EnemyWolf.MOVE_SPEED)
enemy3.add_component(enemy_controller2)
# enemy4 = enemy.clone()

# enemy3 = GameObject("Enemy3", Transform2D(Vector2(1000, -1000), 0, Vector2(1.5, 1.5)), GameObjectType.Dynamic,
#                     GameObjectCategory.Alien)
# enemy3.add_component(BoxCollider2D("Box-4"))
# # enemy.add_component(Rigidbody2D("Rigid"))
# material_enemy = Constants.EnemyAlien.MATERIAL_ENEMY1
# enemy3.add_component(SpriteRenderer2D("enemy3", material_enemy, 1))
# enemy3.add_component(SpriteAnimator2D("enemy3", Constants.EnemyAlien.ENEMY_ANIMATOR_INFO, material_enemy,
#                                       ActiveTake.ENEMY_ALIEN_MOVE_DOWN, Constants.CHARACTER_MOVE_SPEED))
# enemy_controller3 = EnemyController("Enemy movement 3", player, Constants.EnemyAlien.MOVE_SPEED)
# enemy3.add_component(enemy_controller3)
#
# enemy4 = GameObject("Enemy4", Transform2D(Vector2(750, 0), 0, Vector2(1.5, 1.5)), GameObjectType.Dynamic,
#                     GameObjectCategory.Alien)
# enemy4.add_component(BoxCollider2D("Box-5"))
# # enemy.add_component(Rigidbody2D("Rigid"))
# material_enemy = Constants.EnemyAlien.MATERIAL_ENEMY3
# enemy4.add_component(SpriteRenderer2D("enemy4", material_enemy, 1))
# enemy4.add_component(SpriteAnimator2D("enemy4", Constants.EnemyAlien.ENEMY_ANIMATOR_INFO, material_enemy,
#                                       ActiveTake.ENEMY_ALIEN_MOVE_DOWN, Constants.CHARACTER_MOVE_SPEED))
# enemy_controller4 = EnemyController("Enemy movement 4", player, Constants.EnemyAlien.MOVE_SPEED)
# enemy4.add_component(enemy_controller4)
# enemy5 = enemy4.clone()
# enemy6 = enemy4.clone()
# enemy6.transform.translate(20, 20)
# scene.add(enemy5)
# scene.add(enemy6)

text = GameObject("Text", Transform2D(Vector2(0, 0), 0, Vector2(0.2, 0.1)), GameObjectType.Dynamic,
                  GameObjectCategory.Player)
image = pygame.image.load("Assets/UI/Menu/menu_button.png")
texture_material = TextureMaterial2D(image, None, Vector2(0.1, 0.1), None)
text.add_component(Renderer2D("Renderer-2", texture_material, 1))
text.add_component(Renderer2D("Renderer-1", text_material, 2))
text.add_component(BoxCollider2D("Box-2"))

scene.add(player)
scene.add(enemy)

scene_manager.add("Game", scene)
scene_manager.set_active_scene("Game")
renderManager = RendererManager(screen, scene_manager, camera_manager)

# renderManager.is_debug_mode = True


scene.add(enemy2)
scene.add(enemy3)
# scene.add(enemy4)
scene.add(text)
managers.append(camera_manager)
managers.append(scene_manager)

# scene2 = Scene("Test scene")
# scene2.add(text)
# sceneManager.add("Test", scene2)

game_time = GameTime()
# camera_game_object.add_component(ThirdPersonController("Third Person Controller", player))

collider_system = CollisionManager(200, scene_manager, camera_manager)
managers.append(collider_system)

camera_main_menu = Camera("MenuCamera", Constants.VIEWPORT_WIDTH, Constants.VIEWPORT_HEIGHT)
camera_main_menu_game_object = GameObject("MenuCamera", Transform2D(Vector2(0, 0), Vector2(0, 0), Vector2(0, 0)),
                                          GameObjectType.Static, GameObjectCategory.Menu)
camera_main_menu_game_object.add_component(camera_main_menu)

initialise_menu(Constants.Menu.MATERIAL_MAIN_MENU, Constants.GAME_NAME, "Start", "Quit")
# initialise_menu(Constants.Menu.MATERIAL_PAUSE_MENU, "Paused", "Resume", "Main Menu")

for manager in managers:
    if isinstance(manager, IStartable):
        manager.start()
# Fill the screen with a background color
background_color = (0, 0, 0)  # white
if screen is not None:
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

    #
    # if player.lives == 0:
    #     sceneManager.set_active_scene("Test")

    #   text.get_component(BoxCollider2D).draw(screen, cameraManager)

    renderManager.draw(game_time)

    pygame.display.update()
    game_time.limit_fps(60)

pygame.quit()
