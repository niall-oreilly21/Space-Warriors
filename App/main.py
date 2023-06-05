import os
import pygame
from pygame import Vector2

from App.Components.Colliders.PlayerBoxCollider2D import CharacterBoxCollider2D
from App.Components.Colliders.PlayerCollider import PlayerCollider
from App.Components.Controllers.EnemyController import EnemyController
from App.Components.Controllers.PetController import PetController
from App.Constants.Application import Application
from App.Constants.Constants import Constants
from App.Constants.SceneLoader import SceneLoader, initialise_menu
from Engine.GameObjects.Character import Character
from Engine.Managers.CollisionManager import CollisionManager
from Engine.GameObjects.Components.Cameras.ThirdPersonController import ThirdPersonController
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Cameras.Camera import Camera
from Engine.GameObjects.GameObject import GameObjectType, GameObjectCategory, GameObject
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Managers.CameraManager import CameraManager
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Managers.GameStateManager import GameStateManager
from Engine.Managers.SoundManager import SoundManager
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.Enums.RendererLayers import RendererLayers
from Engine.Other.InputHandler import InputHandler
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
from App.Constants.MapLoader import map_load


def load_sound():
    soundManager.load_sound("BackgroundMusic", "Assets/Sounds/background_music.mp3")
    soundManager.set_sound_volume("backgroundmusic", .05)
    Constants.EVENT_DISPATCHER.dispatch_event(
        EventData(EventCategoryType.SoundManager, EventActionType.PlaySound, ["backgroundmusic"]))


def update(game_time):
    earth_scene.update(game_time)


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
pygame.display.set_caption(Constants.GAME_NAME)

camera_game_object = GameObject("MainCamera", Transform2D(Vector2(0, 0), Vector2(0, 0), Vector2(0, 0)),
                                GameObjectType.Dynamic, GameObjectCategory.Player)
camera = Camera("MainCamera", Constants.VIEWPORT_WIDTH, Constants.VIEWPORT_HEIGHT)

camera_game_object.add_component(camera)
managers = []
scene_manager = SceneManager(Constants.EVENT_DISPATCHER)
soundManager = SoundManager(Constants.EVENT_DISPATCHER)

camera_manager = CameraManager(screen, scene_manager, Constants.EVENT_DISPATCHER)

camera_main_menu = Camera("MenuCamera", Constants.VIEWPORT_WIDTH, Constants.VIEWPORT_HEIGHT)
camera_main_menu_game_object = GameObject(Constants.Camera.MENU_CAMERA,
                                          Transform2D(Vector2(0, 0), Vector2(0, 0), Vector2(0, 0)),
                                          GameObjectType.Static, GameObjectCategory.Menu)
camera_main_menu_game_object.add_component(camera_main_menu)

third_person_camera_game_object = camera_main_menu_game_object.clone()
third_person_camera_game_object.name = Constants.Camera.GAME_CAMERA

camera_manager.add(camera_main_menu_game_object)
camera_manager.add(third_person_camera_game_object)

camera_manager.set_active_camera(camera_main_menu_game_object.name)

# Create a font object
font_path = "Assets/Fonts/Starjedi.ttf"
font = pygame.font.Font(font_path, 80)
font_name = font_path

text_material = TextMaterial2D(font, font_name, "Hello, World!", Vector2(150, 40), (255, 0, 0))
sprite_transform = Transform2D(Vector2(10, 100), 0, Vector2(1, 1))

earth_scene = Scene(Constants.Scene.EARTH)
player = Character("Player", Constants.Player.DEFAULT_HEALTH, Constants.Player.DEFAULT_ATTACK_DAMAGE, 2,
                   Constants.Player.TOTAL_LIVES, Transform2D(Vector2(2600, 4900), 0, Vector2(1.2, 1.2)),
                   GameObjectType.Dynamic, GameObjectCategory.Player)

third_person_camera_game_object.add_component(ThirdPersonController("Third Person Controller", player))
player.add_component(Rigidbody2D("Rigid"))
player_box_collider = CharacterBoxCollider2D("Box")
player.add_component(player_box_collider)
material_player = Constants.Player.MATERIAL_GIRL
player.add_component(SpriteRenderer2D("player", material_player, RendererLayers.Player))
player.add_component(SpriteAnimator2D("player", Constants.Player.PLAYER_ANIMATOR_INFO, material_player,
                                      ActiveTake.PLAYER_IDLE_DOWN, Constants.CHARACTER_MOVE_SPEED))
player_controller = PlayerController("Player movement", 0.17, 0.17, player_box_collider)
player.add_component(player_controller)
player_collider = PlayerCollider("Players attack collider")
player.add_component(player_collider)

enemy = Character("Enemy", 70, 1, 1, 1, Transform2D(Vector2(2400, 4500), 0, Vector2(1.5, 1.5)), GameObjectType.Dynamic,
                  GameObjectCategory.Rat)
enemy.add_component(BoxCollider2D("Box-1"))
enemy.add_component(Rigidbody2D("Rigid"))
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
enemy2.add_component(Rigidbody2D("Rigid"))
material_enemy = Constants.EnemyWolf.MATERIAL_ENEMY1
enemy2.add_component(SpriteRenderer2D("enemy2", material_enemy, 1))
enemy2.add_component(SpriteAnimator2D("enemy2", Constants.EnemyWolf.ENEMY_ANIMATOR_INFO, material_enemy,
                                      ActiveTake.ENEMY_WOLF_MOVE_DOWN, Constants.CHARACTER_MOVE_SPEED))
enemy_controller2 = EnemyController("Enemy movement 2", player, Constants.EnemyWolf.MOVE_SPEED)
enemy2.add_component(enemy_controller2)

enemy3 = Character("Enemy3", 50, 2, 1, 1, Transform2D(Vector2(1000, -1000), 0, Vector2(1.5, 1.5)),
                   GameObjectType.Dynamic, GameObjectCategory.Wolf)
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

pet = GameObject("PetDog", Transform2D(Vector2(7210, 5500), 0, Vector2(1.2, 1.2)), GameObjectType.Dynamic,
                 GameObjectCategory.Pet)
material_pet = Constants.PetDog.MATERIAL_PET
pet.add_component(SpriteRenderer2D("PetRenderer", material_pet, RendererLayers.Player))
pet.get_component(SpriteRenderer2D).flip_x = True
pet.add_component(SpriteAnimator2D("PetAnimator", Constants.PetDog.PET_ANIMATOR_INFO, material_pet,
                                   ActiveTake.PET_DOG_SIT, Constants.CHARACTER_MOVE_SPEED))
pet.get_component(SpriteAnimator2D).is_infinite = True
pet.add_component(Rigidbody2D("PetRigidbody"))
pet.add_component(PetController("PetMovement", player, 20))
pet.add_component(BoxCollider2D("PetCollider"))

text = GameObject("Text", Transform2D(Vector2(0, 0), 0, Vector2(0.2, 0.1)), GameObjectType.Dynamic,
                  GameObjectCategory.Player)
image = pygame.image.load("Assets/UI/Menu/menu_button.png")
texture_material = TextureMaterial2D(image, None, Vector2(0.1, 0.1), None)
text.add_component(Renderer2D("Renderer-2", texture_material, 1))
text.add_component(Renderer2D("Renderer-1", text_material, 2))
text.add_component(BoxCollider2D("Box-2"))

earth_scene.add(player)
earth_scene.add(enemy)
earth_scene.add(pet)

mars_scene = Scene(Constants.Scene.MARS)
saturn_scene = Scene(Constants.Scene.SATURN)

scene_manager.add(Constants.Scene.EARTH, earth_scene)
scene_manager.set_active_scene(Constants.Scene.EARTH)
render_manager = RendererManager(screen, scene_manager, camera_manager, Constants.EVENT_DISPATCHER)

scene_manager.add(Constants.Scene.MARS, mars_scene)
scene_manager.add(Constants.Scene.SATURN, saturn_scene)

earth_scene.add(enemy2)
earth_scene.add(enemy3)
# scene.add(enemy4)
# scene.add(text)
managers.append(camera_manager)
managers.append(scene_manager)

# scene2 = Scene("Test scene")
# scene2.add(text)
# sceneManager.add("Test", scene2)

game_time = GameTime()

collider_system = CollisionManager(100, scene_manager, camera_manager)
managers.append(collider_system)

scene_loader = SceneLoader(camera_manager, camera_main_menu_game_object, scene_manager)

pause_menu_scene = scene_loader.initialise_menu_scene(Constants.Scene.PAUSE_MENU)
main_menu_scene = scene_loader.initialise_menu_scene(Constants.Scene.MAIN_MENU)
level_menu_scene = scene_loader.initialise_menu_scene(Constants.Scene.LEVEL_MENU)

initialise_menu(main_menu_scene, Constants.Menu.MATERIAL_MAIN_MENU, Constants.GAME_NAME, "Start", "Quit",
                Constants.Button.START_BUTTON, Constants.Button.QUIT_BUTTON)
initialise_menu(pause_menu_scene, Constants.Menu.MATERIAL_PAUSE_MENU, "Paused", "Resume", "Main Menu",
                Constants.Button.RESUME_BUTTON, Constants.Button.MAIN_MENU_BUTTON)
scene_loader.initialise_level_menu(level_menu_scene)

# scene_manager.set_active_scene(Constants.Scene.PAUSE_MENU)

# scene_manager.add(Constants.Scene.MAIN_MENU, scene)
scene_manager.set_active_scene(Constants.Scene.LEVEL_MENU)
# initialise_level_menu()

game_state_manager = GameStateManager(Constants.EVENT_DISPATCHER, InputHandler())
managers.append(game_state_manager)

Application.ActiveScene = main_menu_scene
Application.ActiveCamera = camera_manager.active_camera

#
# # Load Map + objects
map_load(earth_scene, Constants.Map.PLANET_A_JSON)
map_load(mars_scene, Constants.Map.PLANET_B_JSON)
map_load(saturn_scene, Constants.Map.PLANET_C_JSON)

# load_sound()

for manager in managers:
    manager.start()
# Fill the screen with a background color
background_color = (0, 0, 0)  # black
if screen is not None:
    screen.fill(background_color)
# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game_time.tick()

    Constants.EVENT_DISPATCHER.process_events()

    for manager in managers:
        manager.update(game_time)

    if screen is not None:
        screen.fill(background_color)

    #
    # if player.lives == 0:
    #     sceneManager.set_active_scene("Test")

    #   text.get_component(BoxCollider2D).draw(screen, cameraManager)

    render_manager.draw()

    pygame.display.update()
    game_time.limit_fps(60)

pygame.quit()
