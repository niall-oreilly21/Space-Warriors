import os
import pygame
from pygame import Vector2

from App.Constants.Application import Application
from App.Constants.GameConstants import GameConstants
from App.Constants.EntityConstants import EntityConstants
from App.Constants.GameObjectConstants import GameObjectConstants
from App.Constants.MapLoader import MapLoader
from App.Constants.SceneLoader import SceneLoader, initialise_menu, initialise_level_menu, initialise_character_selection_menu, initialise_controls_menu
from App.Constants.LoadAssets import load_sound, load_fonts, load_cameras
from Engine.Managers.CollisionManager import CollisionManager
from Engine.Managers.CameraManager import CameraManager
from Engine.Managers.EventSystem.EventDispatcher import EventDispatcher
from Engine.Managers.GameStateManager import GameStateManager
from Engine.Managers.SoundManager import SoundManager
from Engine.Other.InputHandler import InputHandler
from Engine.Time.GameTime import GameTime
from Engine.Managers.RendererManager import RendererManager
from Engine.Managers.SceneManager import SceneManager

# Initialize Pygame
pygame.init()

screen_width = 1
screen_height = 1

screen_info = pygame.display.Info()
screen_resolution = Vector2(screen_info.current_w, screen_info.current_h)

os.environ['SDL_VIDEO_CENTERED'] = '1'

screen = pygame.display.set_mode((GameConstants.VIEWPORT_WIDTH, GameConstants.VIEWPORT_HEIGHT))
pygame.display.set_caption(GameConstants.GAME_NAME)

game_time = GameTime()

player = EntityConstants.Player.PLAYER
pet = EntityConstants.Pet.PET

GameConstants.INPUT_HANDLER = InputHandler()
GameConstants.EVENT_DISPATCHER = EventDispatcher()
map_loader = MapLoader(player, GameObjectConstants.HealthBar.PLAYER_HEALTH_BAR, pet, GameObjectConstants.UiHelperTexts.UI_HELPER_TEXTS)

scene_manager = SceneManager(GameConstants.EVENT_DISPATCHER)
sound_manager = SoundManager(GameConstants.EVENT_DISPATCHER)
camera_manager = CameraManager(screen, scene_manager, GameConstants.EVENT_DISPATCHER)
collision_manager = CollisionManager(GameConstants.QuadTree.MAP_DIMENSIONS, player, GameConstants.QuadTree.COLLISION_RANGE_WIDTH, GameConstants.QuadTree.COLLISION_RANGE_HEIGHT, GameConstants.QuadTree.QUAD_TREE_SIZE, GameConstants.EVENT_DISPATCHER)
game_state_manager = GameStateManager(GameConstants.EVENT_DISPATCHER, InputHandler(), map_loader)
render_manager = RendererManager(screen, GameConstants.EVENT_DISPATCHER, GameConstants.QuadTree.MAP_DIMENSIONS, player, GameConstants.VIEWPORT_WIDTH, GameConstants.VIEWPORT_HEIGHT, GameConstants.QuadTree.QUAD_TREE_SIZE)
update_managers = [scene_manager, camera_manager, collision_manager, game_state_manager]

scene_loader = SceneLoader(scene_manager)
earth_scene = scene_loader.initialise_menu_scene(GameConstants.Scene.EARTH)
mars_scene = scene_loader.initialise_menu_scene(GameConstants.Scene.MARS)
saturn_scene = scene_loader.initialise_menu_scene(GameConstants.Scene.SATURN)
house_scene = scene_loader.initialise_menu_scene(GameConstants.Scene.HOUSE)
pause_menu_scene = scene_loader.initialise_menu_scene(GameConstants.Scene.PAUSE_MENU)
main_menu_scene = scene_loader.initialise_menu_scene(GameConstants.Scene.MAIN_MENU)
level_menu_scene = scene_loader.initialise_menu_scene(GameConstants.Scene.LEVEL_MENU)
sound_menu_scene = scene_loader.initialise_menu_scene(GameConstants.Scene.SOUND_MENU)
end_level_menu_scene = scene_loader.initialise_menu_scene(GameConstants.Scene.END_LEVEL_MENU)
character_selection_menu_scene = scene_loader.initialise_menu_scene(GameConstants.Scene.CHARACTER_SELECTION_MENU)
controls_menu_scene = scene_loader.initialise_menu_scene(GameConstants.Scene.CONTROLS_MENU)

initialise_menu(main_menu_scene, GameConstants.Menu.MATERIAL_MAIN_MENU, GameConstants.GAME_NAME,
                [GameConstants.Button.START_BUTTON, GameConstants.Button.CONTROLS_BUTTON, GameConstants.Button.SOUND_BUTTON,
                 GameConstants.Button.QUIT_BUTTON])
initialise_menu(pause_menu_scene, GameConstants.Menu.MATERIAL_PAUSE_MENU, "Paused",
                [GameConstants.Button.RESUME_BUTTON, GameConstants.Button.CONTROLS_BUTTON, GameConstants.Button.MAIN_MENU_BUTTON])
initialise_menu(sound_menu_scene, GameConstants.Menu.MATERIAL_SOUND_MENU, "Sound",
                [GameConstants.Button.MUTE_BUTTON, GameConstants.Button.UNMUTE_BUTTON, GameConstants.Button.MAIN_MENU_BUTTON])
initialise_menu(end_level_menu_scene, GameConstants.Menu.MATERIAL_DEATH_MENU, "You Died",
                [GameConstants.Button.RESTART_BUTTON, GameConstants.Button.LEVELS_BUTTON, GameConstants.Button.MAIN_MENU_BUTTON])
initialise_character_selection_menu(character_selection_menu_scene)
initialise_level_menu(level_menu_scene)
initialise_controls_menu(controls_menu_scene)

load_cameras(camera_manager, player)
load_fonts()
map_loader.map_load(earth_scene, GameConstants.Map.BASE_PATH + GameConstants.Scene.EARTH + GameConstants.Map.JSON_END_PATH)
map_loader.map_load(mars_scene, GameConstants.Map.BASE_PATH + GameConstants.Scene.MARS + GameConstants.Map.JSON_END_PATH)
map_loader.map_load(saturn_scene, GameConstants.Map.BASE_PATH + GameConstants.Scene.SATURN + GameConstants.Map.JSON_END_PATH)
map_loader.map_load(house_scene, GameConstants.Map.BASE_PATH + GameConstants.Scene.HOUSE + GameConstants.Map.JSON_END_PATH)
map_loader.load_planet_earth_enemies(earth_scene)
map_loader.load_planet_mars_enemies(mars_scene)
map_loader.load_planet_saturn_enemies(saturn_scene)
load_sound(sound_manager)

camera_manager.set_active_camera(GameConstants.Cameras.MENU_CAMERA)
scene_manager.set_active_scene(GameConstants.Scene.MAIN_MENU)

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

    for manager in update_managers:
        manager.update(game_time)

    if screen is not None:
        screen.fill(background_color)

    render_manager.draw()

    GameConstants.INPUT_HANDLER.update()
    GameConstants.EVENT_DISPATCHER.process_events()

    pygame.display.update()
    game_time.limit_fps(60)

    # elapsed_time = game_time.elapsed_time
    # fps = game_time.fps()
    # print(f"Elapsed Time: {elapsed_time} ms, FPS: {fps}")

    #print(player.transform.position.x, ", ", player.transform.position.y)

pygame.quit()
