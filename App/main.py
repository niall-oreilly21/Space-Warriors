import os
import pygame
from pygame import Vector2

from App.Components.Colliders.PlayerCollider import PlayerCollider
from App.Components.Controllers.EnemyController import EnemyController
from App.Components.Controllers.PetController import PetController
from App.Constants.Application import Application
from App.Constants.Constants import Constants
from App.Constants.GameObjectConstants import GameObjectConstants
from App.Constants.SceneLoader import SceneLoader, initialise_menu
from Engine.GameObjects.Character import Character
from Engine.GameObjects.Components.Physics.ButtonColliderHover2D import ButtonColliderHover2D
from Engine.GameObjects.Components.Physics.CollisionArea import CollisionArea
from Engine.GameObjects.Components.Physics.WaypointFinder import WaypointFinder
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
    soundManager.load_sound("BackgroundMusicA", "Assets/Sounds/background_music.mp3")
    soundManager.load_sound("BackgroundMusicB", "Assets/Sounds/planet_b_music.wav")
    soundManager.load_sound("BackgroundMusicC", "Assets/Sounds/planet_c_music.mp3")
    soundManager.load_sound("TeleportSound", "Assets/Sounds/teleport.wav")
    soundManager.load_sound("DeathMusic", "Assets/Sounds/death.wav")
    soundManager.load_sound("AttackSound", "Assets/Sounds/sword_swish.wav")
    soundManager.load_sound("BossMusic", "Assets/Sounds/planet_c_music.mp3")
    soundManager.load_sound("ButtonSound", "Assets/Sounds/button.wav")

    soundManager.set_sound_volume("backgroundmusica", .05)
    soundManager.set_sound_volume("backgroundmusicb", .05)
    soundManager.set_sound_volume("backgroundmusicc", .05)
    soundManager.set_sound_volume("attacksound", .05)
    Constants.EVENT_DISPATCHER.dispatch_event(
        EventData(EventCategoryType.SoundManager, EventActionType.PlaySound, ["backgroundmusica"]))


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

sprite_transform = Transform2D(Vector2(10, 100), 0, Vector2(1, 1))

earth_scene = Scene(Constants.Scene.EARTH)
player = Character("Player", Constants.Player.DEFAULT_HEALTH, Constants.Player.DEFAULT_ATTACK_DAMAGE,
                   Constants.Player.DAMAGE_COOLDOWN, Vector2(2900, 4900),
                   Transform2D(Vector2(2900, 4900), 0, Vector2(1.2, 1.2)),
                   GameObjectType.Dynamic, GameObjectCategory.Player)

third_person_camera_game_object.add_component(ThirdPersonController("Third Person Controller", player))
player.add_component(Rigidbody2D("Rigid"))
player_box_collider = BoxCollider2D("Box")
player_box_collider.scale = Vector2(1, 0.5)
player_box_collider.offset = Vector2(0, 20)
player.add_component(player_box_collider)
material_player = Constants.Player.MATERIAL_GIRL
player.add_component(SpriteRenderer2D("player", material_player, RendererLayers.Player))
player.add_component(SpriteAnimator2D("player", Constants.Player.PLAYER_ANIMATOR_INFO, material_player,
                                      ActiveTake.PLAYER_IDLE_DOWN, Constants.CHARACTER_ANIMATOR_MOVE_SPEED))
player_controller = PlayerController("Player movement", Constants.Player.MOVE_SPEED, Constants.Player.MOVE_SPEED,
                                     player_box_collider)
player.add_component(player_controller)
player_collider = PlayerCollider("Players attack collider")
player.add_component(player_collider)

enemy = Character("Enemy", 70, 100, 1, Vector2(2400, 4500), Transform2D(Vector2(2400, 4500), 0, Vector2(1.5, 1.5)),
                  GameObjectType.Dynamic, GameObjectCategory.Rat)
enemy.add_component(BoxCollider2D("Box-1"))
enemy.add_component(Rigidbody2D("Rigid"))
material_enemy = Constants.EnemyRat.MATERIAL_ENEMY1
enemy.add_component(SpriteRenderer2D("enemy", material_enemy, 0))
enemy.add_component(SpriteAnimator2D("enemy", Constants.EnemyRat.ENEMY_ANIMATOR_INFO, material_enemy,
                                     ActiveTake.ENEMY_RAT_MOVE_DOWN, Constants.CHARACTER_ANIMATOR_MOVE_SPEED))
enemy_controller = EnemyController("Enemy movement", player, Constants.EnemyRat.MOVE_SPEED, 200)
enemy.add_component(enemy_controller)
enemy.add_component(WaypointFinder("Waypoint finder", [Vector2(2000, 4500), Vector2(2200, 4500), Vector2(2400, 4500),
                                                       Vector2(2800, 4500)]))

enemy2 = Character("Enemy2", 50, 2, 1, Transform2D(Vector2(-1000, -1000), 0, Vector2(1.5, 1.5)),
                   GameObjectType.Dynamic,
                   GameObjectCategory.Wolf)
enemy2.add_component(BoxCollider2D("Box-3"))
enemy2.add_component(Rigidbody2D("Rigid"))
material_enemy = Constants.EnemyWolf.MATERIAL_ENEMY1
enemy2.add_component(SpriteRenderer2D("enemy2", material_enemy, 1))
enemy2.add_component(SpriteAnimator2D("enemy2", Constants.EnemyWolf.ENEMY_ANIMATOR_INFO, material_enemy,
                                      ActiveTake.ENEMY_WOLF_MOVE_DOWN, Constants.CHARACTER_ANIMATOR_MOVE_SPEED))
enemy_controller2 = EnemyController("Enemy movement 2", player, Constants.EnemyWolf.MOVE_SPEED, 600)
enemy2.add_component(enemy_controller2)

enemy3 = Character("Enemy3", 50, 2, 1, Vector2(1000, -1000), Transform2D(Vector2(1000, -1000), 0, Vector2(1.5, 1.5)),
                   GameObjectType.Dynamic, GameObjectCategory.Wolf)
enemy3.add_component(BoxCollider2D("Box-3"))
# enemy.add_component(Rigidbody2D("Rigid"))
material_enemy = Constants.EnemyWolf.MATERIAL_ENEMY3
enemy3.add_component(SpriteRenderer2D("enemy2", material_enemy, 1))
enemy3.add_component(SpriteAnimator2D("enemy2", Constants.EnemyWolf.ENEMY_ANIMATOR_INFO, material_enemy,
                                      ActiveTake.ENEMY_WOLF_MOVE_DOWN, Constants.CHARACTER_ANIMATOR_MOVE_SPEED))
enemy_controller2 = EnemyController("Enemy movement 2", player, Constants.EnemyWolf.MOVE_SPEED, 600)
enemy3.add_component(enemy_controller2)
# enemy4 = enemy.clone()

pet = GameObject("PetDog", Transform2D(Vector2(7210, 5500), 0, Vector2(1.2, 1.2)), GameObjectType.Dynamic,
                 GameObjectCategory.Pet)

material_pet = Constants.PetDog.MATERIAL_PET
pet.add_component(SpriteRenderer2D("PetRenderer", material_pet, RendererLayers.Player))
pet.get_component(SpriteRenderer2D).flip_x = True
pet.add_component(SpriteAnimator2D("PetAnimator", Constants.PetDog.PET_ANIMATOR_INFO, material_pet,
                                   ActiveTake.PET_DOG_SIT, Constants.CHARACTER_ANIMATOR_MOVE_SPEED))
pet.get_component(SpriteAnimator2D).is_infinite = True
pet.add_component(Rigidbody2D("PetRigidbody"))
pet.add_component(PetController("PetMovement", player, 25))
pet_collider = BoxCollider2D("PetCollider")
pet_collider.scale = Vector2(2.5, 2.5)
pet.add_component(pet_collider)

# Create a font object
font_path = "Assets/Fonts/VCR_OSD_MONO.ttf"

text_material = TextMaterial2D(font_path, 40, "", Vector2(Constants.VIEWPORT_WIDTH / 2, 700), (255, 255, 255))
ui_text_helper = GameObject("UITextHelper", Transform2D(Vector2(0, 0), 0, Vector2(1, 1)), GameObjectType.Static,
                            GameObjectCategory.UI)
image = pygame.image.load("Assets/UI/Menu/menu_button.png")
ui_text_helper.add_component(Renderer2D("Renderer-1", text_material, RendererLayers.UI))

text_material_top_right = TextMaterial2D(font_path, 30, "Hello", Vector2(Constants.VIEWPORT_WIDTH - 150, 75),
                                         (255, 255, 255))
ui_text_helper_top_right = GameObject("UITextHelperTopRight", Transform2D(Vector2(0, 0), 0, Vector2(1, 1)),
                                      GameObjectType.Static, GameObjectCategory.UI)
ui_text_helper_top_right.add_component(Renderer2D("Renderer-2", text_material_top_right, RendererLayers.UI))

# ui_text_helper_component = UITextHelper("UI text helper")
# ui_text_helper.add_component(ui_text_helper_component)


earth_scene.add(enemy)
earth_scene.add(pet)
earth_scene.add(ui_text_helper)
earth_scene.add(ui_text_helper_top_right)

mars_scene = Scene(Constants.Scene.MARS)
saturn_scene = Scene(Constants.Scene.SATURN)

scene_manager.add(Constants.Scene.EARTH, earth_scene)
scene_manager.set_active_scene(Constants.Scene.EARTH)
render_manager = RendererManager(screen, scene_manager, camera_manager, Constants.EVENT_DISPATCHER)

scene_manager.add(Constants.Scene.MARS, mars_scene)
scene_manager.add(Constants.Scene.SATURN, saturn_scene)

earth_scene.add(player)
earth_scene.add(GameObjectConstants.HealthBar.HEALTH_BAR)
# earth_scene.add(enemy2)
# earth_scene.add(enemy3)
# scene.add(enemy4)
# scene.add(text)
managers.append(camera_manager)
managers.append(scene_manager)

# scene2 = Scene("Test scene")
# scene2.add(text)
# sceneManager.add("Test", scene2)

game_time = GameTime()

collider_system = CollisionManager(100, scene_manager, camera_manager, Constants.EVENT_DISPATCHER)
managers.append(collider_system)

scene_loader = SceneLoader(camera_manager, camera_main_menu_game_object, scene_manager)

pause_menu_scene = scene_loader.initialise_menu_scene(Constants.Scene.PAUSE_MENU)
main_menu_scene = scene_loader.initialise_menu_scene(Constants.Scene.MAIN_MENU)
level_menu_scene = scene_loader.initialise_menu_scene(Constants.Scene.LEVEL_MENU)
sound_menu_scene = scene_loader.initialise_menu_scene(Constants.Scene.SOUND_MENU)
death_menu_scene = scene_loader.initialise_menu_scene(Constants.Scene.DEATH_MENU)

initialise_menu(main_menu_scene, Constants.Menu.MATERIAL_MAIN_MENU, Constants.GAME_NAME,
                [Constants.Button.START_BUTTON, Constants.Button.SOUND_BUTTON, Constants.Button.QUIT_BUTTON])
initialise_menu(pause_menu_scene, Constants.Menu.MATERIAL_PAUSE_MENU, "Paused",
                [Constants.Button.RESUME_BUTTON, Constants.Button.MAIN_MENU_BUTTON])
initialise_menu(sound_menu_scene, Constants.Menu.MATERIAL_SOUND_MENU, "Sound",
                [Constants.Button.MUTE_BUTTON, Constants.Button.UNMUTE_BUTTON, Constants.Button.MAIN_MENU_BUTTON])
initialise_menu(death_menu_scene, Constants.Menu.MATERIAL_DEATH_MENU, "You Died",
                [Constants.Button.RESTART_BUTTON, Constants.Button.MAIN_MENU_BUTTON])
scene_loader.initialise_level_menu(level_menu_scene)

# scene_manager.set_active_scene(Constants.Scene.PAUSE_MENU)

# scene_manager.add(Constants.Scene.MAIN_MENU, scene)
scene_manager.set_active_scene(Constants.Scene.LEVEL_MENU)
# initialise_level_menu()

game_state_manager = GameStateManager(Constants.EVENT_DISPATCHER, InputHandler(), ui_text_helper)
managers.append(game_state_manager)

Application.ActiveScene = main_menu_scene
Application.ActiveCamera = camera_manager.active_camera
Application.Player = player
Constants.INPUT_HANDLER = InputHandler()

#
# # Load Map + objects
map_load(earth_scene, Constants.Map.PLANET_A_JSON)
# map_load(mars_scene, Constants.Map.PLANET_B_JSON)
# map_load(saturn_scene, Constants.Map.PLANET_C_JSON)

load_sound()

for manager in managers:
    manager.start()

# Fill the screen with a background color
background_color = (0, 0, 0)  # black
if screen is not None:
    screen.fill(background_color)

render_manager.is_debug_mode = True

# Grid dimensions
grid_size = 110
grid_width = 72
grid_height = 72


# Create the grid
# grid = {}
# for row in range(grid_size):
#     for col in range(grid_size):
#         rect = pygame.Rect(col * grid_width, row * grid_height, grid_width, grid_height)
#         grid[(row, col)] = rect


def update_collision_area():
    camera = camera_manager.active_camera

    viewport = camera.viewport
    camera_position = camera.parent.transform.position

    return CollisionArea(2150 - camera_position.x, 4525 - camera_position.y, 1500, 750)


water_collsion_boxes = earth_scene.get_all_components_by_type(BoxCollider2D)

print("Colliders", len(water_collsion_boxes))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game_time.tick()

    Constants.INPUT_HANDLER.update()
    Constants.EVENT_DISPATCHER.process_events()

    Constants.EVENT_DISPATCHER.dispatch_event(
        EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,
                  [""]))

    for manager in managers:
        manager.update(game_time)

    if screen is not None:
        screen.fill(background_color)

    render_manager.draw()

    colision_area = update_collision_area()

    colliders = earth_scene.get_all_components_by_type(BoxCollider2D)

    # for collider in colliders:
    #     if collider.parent.name == "Player":
    #         print(collider.bounds)
    #
    # print()
    # print()

    # print(colision_area.boundary)
    # pygame.draw.rect(screen, (255, 255, 255), colision_area.boundary)
    # print("player: ", player.transform.position.x, ", ", player.transform.position.y )

    draw_x = collider_system.collision_area.boundary.x - Application.ActiveCamera.transform.position.x
    draw_y = collider_system.collision_area.boundary.y - Application.ActiveCamera.transform.position.y

    rect = pygame.Rect(draw_x, draw_y, collider_system.collision_area.boundary.width,
                       collider_system.collision_area.boundary.height)

    pygame.draw.rect(screen, (255, 255, 255), rect, 5)

    print("Speed: ", player.get_component(PlayerController).speed, ", Damage cooldown: ", player.damage_cooldown,
          ", Attack damage: ", player.attack_damage)

    # # Draw the grid
    # for rect in grid.values():
    #     pygame.draw.rect(screen, (255, 255, 255), rect, 1)

    pygame.display.update()
    game_time.limit_fps(60)

pygame.quit()
