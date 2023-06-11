from pygame import Vector2
from App.Constants.Constants import Constants
from App.Constants.GameObjectConstants import GameObjectConstants
from Engine.GameObjects.Components.Cameras.ThirdPersonController import ThirdPersonController
from Engine.Graphics.Materials.TextMaterial2D import TextMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.Enums.RendererLayers import RendererLayers


def load_sound(sound_manager):
    sound_manager.load_sound(Constants.Music.MENU_MUSIC, Constants.MusicFilePath.MENU_MUSIC_FILEPATH)
    sound_manager.load_sound(Constants.Music.BACKGROUND_MUSIC_EARTH, Constants.MusicFilePath.BACKGROUND_MUSIC_EARTH_FILEPATH)
    sound_manager.load_sound(Constants.Music.BACKGROUND_MUSIC_MARS, Constants.MusicFilePath.BACKGROUND_MUSIC_MARS_FILEPATH)
    sound_manager.load_sound(Constants.Music.BACKGROUND_MUSIC_SATURN, Constants.MusicFilePath.BACKGROUND_MUSIC_SATURN_FILEPATH)
    sound_manager.load_sound(Constants.Music.TELEPORT_SOUND, Constants.MusicFilePath.TELEPORT_SOUND_FILEPATH)
    sound_manager.load_sound(Constants.Music.PLAYER_DEATH_SOUND, Constants.MusicFilePath.PLAYER_DEATH_SOUND_FILEPATH)
    sound_manager.load_sound(Constants.Music.PLAYER_ATTACK_SOUND, Constants.MusicFilePath.PLAYER_ATTACK_SOUND_FILEPATH)
    sound_manager.load_sound(Constants.Music.BUTTON_SOUND, Constants.MusicFilePath.BUTTON_SOUND_FILEPATH)
    sound_manager.load_sound(Constants.Music.POTION_DRINK_SOUND, Constants.MusicFilePath.POTION_DRINK_SOUND_FILEPATH)
    sound_manager.load_sound(Constants.Music.ENEMY_DEATH_SOUND, Constants.MusicFilePath.ENEMY_DEATH_SOUND_FILEPATH)
    sound_manager.load_sound(Constants.Music.ZAP_SOUND, Constants.MusicFilePath.ZAP_SOUND_FILEPATH)
    sound_manager.load_sound(Constants.Music.BULLET_SOUND, Constants.MusicFilePath.BULLET_SOUND_FILEPATH)
    sound_manager.set_sound_volume(Constants.Music.MENU_MUSIC, .05)
    sound_manager.set_sound_volume(Constants.Music.BACKGROUND_MUSIC_EARTH, .05)
    sound_manager.set_sound_volume(Constants.Music.BACKGROUND_MUSIC_MARS, .05)
    sound_manager.set_sound_volume(Constants.Music.BACKGROUND_MUSIC_SATURN, .05)
    sound_manager.set_sound_volume(Constants.Music.PLAYER_ATTACK_SOUND, .05)
    sound_manager.set_sound_volume(Constants.Music.POTION_DRINK_SOUND, 1)
    Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SoundManager, EventActionType.PlaySound, [Constants.Music.MENU_MUSIC]))

def load_cameras(camera_manager, player):
    camera_manager.add(GameObjectConstants.Cameras.MAIN_MENU_CAMERA)
    camera_manager.add(GameObjectConstants.Cameras.GAME_CAMERA)
    GameObjectConstants.Cameras.GAME_CAMERA.add_component(ThirdPersonController("Third Person Controller", player))


def load_fonts():
    TEXT_MATERIAL_UI_TEXT_HELPER_BOTTOM = TextMaterial2D(GameObjectConstants.UiHelperTexts.UI_HELPER_TEXT_FONT_PATH, 40,
                                                         "",
                                                         Vector2(Constants.VIEWPORT_WIDTH / 2, 700),
                                                         (255, 255, 255))
    TEXT_MATERIAL_UI_TEXT_HELPER_RIGHT = TextMaterial2D(GameObjectConstants.UiHelperTexts.UI_HELPER_TEXT_FONT_PATH, 30,
                                                        "",
                                                        Vector2(Constants.VIEWPORT_WIDTH - 150, 75),
                                                        (255, 255, 255))
    GameObjectConstants.UiHelperTexts.UI_TEXT_HELPER_BOTTOM.add_component(
        Renderer2D("Renderer-1", TEXT_MATERIAL_UI_TEXT_HELPER_BOTTOM, RendererLayers.UI))
    GameObjectConstants.UiHelperTexts.UI_TEXT_HELPER_RIGHT.add_component(
        Renderer2D("Renderer-2", TEXT_MATERIAL_UI_TEXT_HELPER_RIGHT, RendererLayers.UI))








