import os
import pygame
from pygame import Vector2

from App.Constants.Application import Application
from App.Constants.Constants import Constants
from App.Constants.EntityConstants import EntityConstants
from App.Constants.GameObjectConstants import GameObjectConstants
from App.Constants.MapLoader import MapLoader
from App.Constants.SceneLoader import SceneLoader, initialise_menu, initialise_level_menu, initialise_character_selection_menu, initialise_controls_menu
from App.Constants.LoadAssets import load_sound, load_fonts, load_map, load_cameras
from Engine.Managers.CollisionManager import CollisionManager
from Engine.Managers.CameraManager import CameraManager
from Engine.Managers.EventSystem.EventDispatcher import EventDispatcher
from Engine.Managers.GameStateManager import GameStateManager
from Engine.Managers.SoundManager import SoundManager
from Engine.Other.InputHandler import InputHandler
from Engine.Time.GameTime import GameTime
from Engine.Managers.RendererManager import RendererManager
from Engine.Managers.Scene import Scene
from Engine.Managers.SceneManager import SceneManager

# Initialize Pygame
pygame.init()

screen_width = 1
screen_height = 1

screen_info = pygame.display.Info()
screen_resolution = Vector2(screen_info.current_w, screen_info.current_h)

os.environ['SDL_VIDEO_CENTERED'] = '1'

screen = pygame.display.set_mode((Constants.VIEWPORT_WIDTH, Constants.VIEWPORT_HEIGHT))
pygame.display.set_caption(Constants.GAME_NAME)

game_time = GameTime()

player = EntityConstants.Player.PLAYER
pet = EntityConstants.Pet.PET

Constants.INPUT_HANDLER = InputHandler()
Constants.EVENT_DISPATCHER = EventDispatcher()
map_loader = MapLoader(player, GameObjectConstants.HealthBar.HEALTH_BAR, pet, GameObjectConstants.UiHelperTexts.UI_HELPER_TEXTS)

scene_manager = SceneManager(Constants.EVENT_DISPATCHER)
sound_manager = SoundManager(Constants.EVENT_DISPATCHER)
camera_manager = CameraManager(screen, scene_manager, Constants.EVENT_DISPATCHER)
collision_manager = CollisionManager(Constants.QuadTree.MAP_DIMENSIONS, player, Constants.QuadTree.COLLISION_RANGE_WIDTH, Constants.QuadTree.COLLISION_RANGE_HEIGHT, Constants.QuadTree.QUAD_TREE_SIZE, Constants.EVENT_DISPATCHER)
game_state_manager = GameStateManager(Constants.EVENT_DISPATCHER, InputHandler(), map_loader)
render_manager = RendererManager(screen, Constants.EVENT_DISPATCHER, Constants.QuadTree.MAP_DIMENSIONS, player, Constants.VIEWPORT_WIDTH + 10, Constants.VIEWPORT_HEIGHT + 10, Constants.QuadTree.QUAD_TREE_SIZE)
managers = [scene_manager, camera_manager, collision_manager, game_state_manager]

earth_scene = Scene(Constants.Scene.EARTH)
mars_scene = Scene(Constants.Scene.MARS)
saturn_scene = Scene(Constants.Scene.SATURN)

scene_manager.add(Constants.Scene.EARTH, earth_scene)
scene_manager.add(Constants.Scene.MARS, mars_scene)
scene_manager.add(Constants.Scene.SATURN, saturn_scene)

load_cameras(camera_manager, player)
load_fonts()
load_map(map_loader, (earth_scene, mars_scene, saturn_scene))
load_sound(sound_manager)

scene_loader = SceneLoader(camera_manager, GameObjectConstants.Cameras.MAIN_MENU_CAMERA, scene_manager)

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

camera_manager.set_active_camera(Constants.Cameras.MENU_CAMERA)
scene_manager.set_active_scene(Constants.Scene.MAIN_MENU)

Application.ActiveScene = main_menu_scene
Application.ActiveCamera = camera_manager.active_camera
Application.Player = player

scene_manager.start()
camera_manager.start()

background_color = (0, 0, 0)

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

    render_manager.draw()

    Constants.INPUT_HANDLER.update()
    Constants.EVENT_DISPATCHER.process_events()

    pygame.display.update()
    game_time.limit_fps(60)

pygame.quit()
