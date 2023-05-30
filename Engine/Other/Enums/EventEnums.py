class EventCategoryType:
    SceneManager = 0
    CameraManager = 1
    SoundManager = 2
    RendererManager = 3


class EventActionType:
    MainMenuScene = 0
    GameMenuScene = 1
    MenuCamera = 2
    GameCamera = 3
    PlaySound = 4
    StopSound = 5
    StopAllSounds = 6
    SetSoundVolume = 7
    SetSoundMasterVolume = 8
    ExitGame = 9