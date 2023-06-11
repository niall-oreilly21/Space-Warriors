import os
import pygame

from App.Components.Colliders.PlayerCollider import PlayerCollider
from App.Components.Controllers.HealthBarController import HealthBarController
from App.Components.Controllers.PetController import PetController
from App.Constants.Application import Application
from App.Constants.SceneLoader import SceneLoader, initialise_menu, initialise_level_menu, \
    initialise_character_selection_menu, initialise_controls_menu
from App.Constants.LoadAssets import load_sound, load_fonts, load_map
from Engine.GameObjects.Character import Character
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Managers.CollisionManager import CollisionManager
from Engine.GameObjects.Components.Cameras.ThirdPersonController import ThirdPersonController
from Engine.GameObjects.Components.Cameras.Camera import Camera
from Engine.GameObjects.GameObject import GameObject
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Managers.CameraManager import CameraManager
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Managers.GameStateManager import GameStateManager
from Engine.Managers.SoundManager import SoundManager
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.InputHandler import InputHandler
from Engine.Time.GameTime import GameTime
from App.Components.Controllers.PlayerController import PlayerController
from Engine.Managers.RendererManager import RendererManager
from Engine.Managers.Scene import Scene
from Engine.Managers.SceneManager import SceneManager
from Engine.Graphics.Materials.TextMaterial2D import TextMaterial2D
from App.Constants.MapLoader import *

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
sound_manager = SoundManager(Constants.EVENT_DISPATCHER)

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

pet = GameObject("PetDog", Transform2D(Vector2(7210, 5500), 0, Vector2(1.2, 1.2)), GameObjectType.Dynamic,GameObjectCategory.Pet)

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
image = pygame.image.load("Assets/UI/Menu/menu_button.png")

earth_scene.add(pet)
mars_scene = Scene(Constants.Scene.MARS)
saturn_scene = Scene(Constants.Scene.SATURN)

scene_manager.add(Constants.Scene.EARTH, earth_scene)
render_manager = RendererManager(screen, Constants.EVENT_DISPATCHER, pygame.Rect(0, 0, 110 * 72, 120 * 72), player,
                                 Constants.VIEWPORT_WIDTH + 10, Constants.VIEWPORT_HEIGHT + 10, 4)
scene_manager.add(Constants.Scene.MARS, mars_scene)
scene_manager.add(Constants.Scene.SATURN, saturn_scene)

earth_scene.add(GameObjectConstants.HealthBar.HEALTH_BAR)
managers.append(camera_manager)
managers.append(scene_manager)

game_time = GameTime()

collider_system = CollisionManager(pygame.Rect(0, 0, 110 * 72, 120 * 72), player, 400, 400, 4, Constants.EVENT_DISPATCHER)
managers.append(collider_system)

scene_loader = SceneLoader(camera_manager, camera_main_menu_game_object, scene_manager)

pause_menu_scene = scene_loader.initialise_menu_scene(Constants.Scene.PAUSE_MENU)
main_menu_scene = scene_loader.initialise_menu_scene(Constants.Scene.MAIN_MENU)
level_menu_scene = scene_loader.initialise_menu_scene(Constants.Scene.LEVEL_MENU)
sound_menu_scene = scene_loader.initialise_menu_scene(Constants.Scene.SOUND_MENU)
death_menu_scene = scene_loader.initialise_menu_scene(Constants.Scene.DEATH_MENU)
character_selection_menu_scene = scene_loader.initialise_menu_scene(Constants.Scene.CHARACTER_SELECTION_MENU)
controls_menu_scene = scene_loader.initialise_menu_scene(Constants.Scene.CONTROLS_MENU)

initialise_menu(main_menu_scene, Constants.Menu.MATERIAL_MAIN_MENU, Constants.GAME_NAME,
                [Constants.Button.START_BUTTON, Constants.Button.CONTROLS_BUTTON, Constants.Button.SOUND_BUTTON,
                 Constants.Button.QUIT_BUTTON])
initialise_menu(pause_menu_scene, Constants.Menu.MATERIAL_PAUSE_MENU, "Paused",
                [Constants.Button.RESUME_BUTTON, Constants.Button.LEVELS_BUTTON, Constants.Button.MAIN_MENU_BUTTON])
initialise_menu(sound_menu_scene, Constants.Menu.MATERIAL_SOUND_MENU, "Sound",
                [Constants.Button.MUTE_BUTTON, Constants.Button.UNMUTE_BUTTON, Constants.Button.MAIN_MENU_BUTTON])
initialise_menu(death_menu_scene, Constants.Menu.MATERIAL_DEATH_MENU, "You Died",
                [Constants.Button.RESTART_BUTTON, Constants.Button.MAIN_MENU_BUTTON])
initialise_character_selection_menu(character_selection_menu_scene)
initialise_level_menu(level_menu_scene)
initialise_controls_menu(controls_menu_scene)

scene_manager.set_active_scene(Constants.Scene.MAIN_MENU)

load_fonts()
map_loader = MapLoader(player, GameObjectConstants.HealthBar.HEALTH_BAR, pet, GameObjectConstants.UiHelperTexts.UI_HELPER_TEXTS)

game_state_manager = GameStateManager(Constants.EVENT_DISPATCHER, InputHandler(), map_loader)
managers.append(game_state_manager)

Application.ActiveScene = main_menu_scene
Application.ActiveCamera = camera_manager.active_camera
Application.Player = player

Constants.INPUT_HANDLER = InputHandler()

load_map(map_loader, (earth_scene, mars_scene, saturn_scene))
load_sound(sound_manager)


scene_manager.start()
camera_manager.start()

# Fill the screen with a background color
background_color = (0, 0, 0)  # black
if screen is not None:
    screen.fill(background_color)

render_manager.is_debug_mode = True

Application.GameStarted = True
# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game_time.tick()

    Constants.EVENT_DISPATCHER.dispatch_event(
        EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper, ["", Constants.UITextPrompts.UI_TEXT_BOTTOM]))

    for manager in managers:
        manager.update(game_time)

    if screen is not None:
        screen.fill(background_color)

    render_manager.draw()

    Constants.INPUT_HANDLER.update()
    Constants.EVENT_DISPATCHER.process_events()

    # elapsed_time = game_time.elapsed_time
    # fps = game_time.fps()
    # print(f"Elapsed Time: {elapsed_time} ms, FPS: {fps}")

    pygame.display.update()
    game_time.limit_fps(60)

pygame.quit()
