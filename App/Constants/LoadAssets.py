from pygame import Vector2
from App.Constants.GameConstants import GameConstants
from App.Constants.GameObjectConstants import GameObjectConstants
from Engine.GameObjects.Components.Cameras.ThirdPersonController import ThirdPersonController
from Engine.Graphics.Materials.TextMaterial2D import TextMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.Enums.RendererLayers import RendererLayers


def load_sound(sound_manager):
    sound_manager.load_sound(GameConstants.Music.MENU_MUSIC, GameConstants.MusicFilePath.MENU_MUSIC_FILEPATH)
    sound_manager.load_sound(GameConstants.Music.BACKGROUND_MUSIC_EARTH, GameConstants.MusicFilePath.BACKGROUND_MUSIC_EARTH_FILEPATH)
    sound_manager.load_sound(GameConstants.Music.BACKGROUND_MUSIC_MARS, GameConstants.MusicFilePath.BACKGROUND_MUSIC_MARS_FILEPATH)
    sound_manager.load_sound(GameConstants.Music.BACKGROUND_MUSIC_SATURN, GameConstants.MusicFilePath.BACKGROUND_MUSIC_SATURN_FILEPATH)
    sound_manager.load_sound(GameConstants.Music.TELEPORT_SOUND, GameConstants.MusicFilePath.TELEPORT_SOUND_FILEPATH)
    sound_manager.load_sound(GameConstants.Music.PLAYER_DEATH_SOUND, GameConstants.MusicFilePath.PLAYER_DEATH_SOUND_FILEPATH)
    sound_manager.load_sound(GameConstants.Music.PLAYER_ATTACK_SOUND, GameConstants.MusicFilePath.PLAYER_ATTACK_SOUND_FILEPATH)
    sound_manager.load_sound(GameConstants.Music.BUTTON_SOUND, GameConstants.MusicFilePath.BUTTON_SOUND_FILEPATH)
    sound_manager.load_sound(GameConstants.Music.POTION_DRINK_SOUND, GameConstants.MusicFilePath.POTION_DRINK_SOUND_FILEPATH)
    sound_manager.load_sound(GameConstants.Music.ENEMY_DEATH_SOUND, GameConstants.MusicFilePath.ENEMY_DEATH_SOUND_FILEPATH)
    sound_manager.load_sound(GameConstants.Music.ZAP_SOUND, GameConstants.MusicFilePath.ZAP_SOUND_FILEPATH)
    sound_manager.load_sound(GameConstants.Music.BULLET_SOUND, GameConstants.MusicFilePath.BULLET_SOUND_FILEPATH)
    sound_manager.load_sound(GameConstants.Music.DOG_BARK_SOUND, GameConstants.MusicFilePath.DOG_BARK_SOUND_FILEPATH)
    sound_manager.load_sound(GameConstants.Music.DOOR_SOUND, GameConstants.MusicFilePath.DOOR_SOUND_FILEPATH)
    sound_manager.load_sound(GameConstants.Music.ENEMY_ATTACK_SOUND, GameConstants.MusicFilePath.ENEMY_ATTACK_SOUND_FILEPATH)
    sound_manager.load_sound(GameConstants.Music.FOOTSTEP_SOUND, GameConstants.MusicFilePath.FOOTSTEP_SOUND_FILEPATH)
    sound_manager.set_sound_volume(GameConstants.Music.MENU_MUSIC, .05)
    sound_manager.set_sound_volume(GameConstants.Music.BACKGROUND_MUSIC_EARTH, .05)
    sound_manager.set_sound_volume(GameConstants.Music.BACKGROUND_MUSIC_MARS, .05)
    sound_manager.set_sound_volume(GameConstants.Music.BACKGROUND_MUSIC_SATURN, .05)
    sound_manager.set_sound_volume(GameConstants.Music.PLAYER_ATTACK_SOUND, .05)
    sound_manager.set_sound_volume(GameConstants.Music.POTION_DRINK_SOUND, 1)
    GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SoundManager, EventActionType.PlaySound, [GameConstants.Music.MENU_MUSIC]))

def load_cameras(camera_manager, player):
    camera_manager.add(GameObjectConstants.Cameras.MAIN_MENU_CAMERA)
    camera_manager.add(GameObjectConstants.Cameras.GAME_CAMERA)
    GameObjectConstants.Cameras.GAME_CAMERA.add_component(ThirdPersonController("Third Person Controller", player))


def load_fonts():
    TEXT_MATERIAL_UI_TEXT_HELPER_BOTTOM = TextMaterial2D(GameObjectConstants.UiHelperTexts.UI_HELPER_TEXT_FONT_PATH, 40,
                                                         "",
                                                         Vector2(GameConstants.VIEWPORT_WIDTH / 2, 700),
                                                         (255, 255, 255))
    TEXT_MATERIAL_UI_TEXT_HELPER_ENEMY_COUNT = TextMaterial2D(GameObjectConstants.UiHelperTexts.UI_HELPER_TEXT_FONT_PATH, 30,
                                                        "",
                                                        Vector2(GameConstants.VIEWPORT_WIDTH - 175, 75),
                                                        (255, 255, 255))
    TEXT_MATERIAL_UI_TEXT_HELPER_RIGHT = TextMaterial2D(GameObjectConstants.UiHelperTexts.UI_HELPER_TEXT_FONT_PATH, 30,
                                                        "",
                                                        Vector2(GameConstants.VIEWPORT_WIDTH - 175, 145),
                                                        (255, 255, 255))
    GameObjectConstants.UiHelperTexts.UI_TEXT_HELPER_BOTTOM.add_component(
        Renderer2D("Renderer-1", TEXT_MATERIAL_UI_TEXT_HELPER_BOTTOM, RendererLayers.UI))
    GameObjectConstants.UiHelperTexts.UI_TEXT_HELPER_ENEMY_COUNT.add_component(
        Renderer2D("Renderer-2", TEXT_MATERIAL_UI_TEXT_HELPER_ENEMY_COUNT, RendererLayers.UI))
    GameObjectConstants.UiHelperTexts.UI_TEXT_HELPER_RIGHT.add_component(
        Renderer2D("Renderer-3", TEXT_MATERIAL_UI_TEXT_HELPER_RIGHT, RendererLayers.UI))









