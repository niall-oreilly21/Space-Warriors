from App.Constants.Constants import Constants
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType


def load_sound(soundManager):
    soundManager.load_sound(Constants.Music.MENU_MUSIC, Constants.MusicFilePath.MENU_MUSIC_FILEPATH)
    soundManager.load_sound(Constants.Music.BACKGROUND_MUSIC_A, Constants.MusicFilePath.BACKGROUND_MUSIC_A_FILEPATH)
    soundManager.load_sound(Constants.Music.BACKGROUND_MUSIC_B, Constants.MusicFilePath.BACKGROUND_MUSIC_B_FILEPATH)
    soundManager.load_sound(Constants.Music.BACKGROUND_MUSIC_C, Constants.MusicFilePath.BACKGROUND_MUSIC_C_FILEPATH)
    soundManager.load_sound(Constants.Music.TELEPORT_SOUND, Constants.MusicFilePath.TELEPORT_SOUND_FILEPATH)
    soundManager.load_sound(Constants.Music.PLAYER_DEATH_SOUND, Constants.MusicFilePath.PLAYER_DEATH_SOUND_FILEPATH)
    soundManager.load_sound(Constants.Music.PLAYER_ATTACK_SOUND, Constants.MusicFilePath.PLAYER_ATTACK_SOUND_FILEPATH)
    soundManager.load_sound(Constants.Music.BUTTON_SOUND, Constants.MusicFilePath.BUTTON_SOUND_FILEPATH)

    soundManager.set_sound_volume(Constants.Music.MENU_MUSIC, .05)
    soundManager.set_sound_volume(Constants.Music.BACKGROUND_MUSIC_A, .05)
    soundManager.set_sound_volume(Constants.Music.BACKGROUND_MUSIC_B, .05)
    soundManager.set_sound_volume(Constants.Music.BACKGROUND_MUSIC_C, .05)
    soundManager.set_sound_volume(Constants.Music.PLAYER_ATTACK_SOUND, .05)
    Constants.EVENT_DISPATCHER.dispatch_event(
        EventData(EventCategoryType.SoundManager, EventActionType.PlaySound, [Constants.Music.MENU_MUSIC]))
