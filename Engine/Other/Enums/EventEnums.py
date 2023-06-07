class EventCategoryType:
    SceneManager = 0
    CameraManager = 1
    SoundManager = 2
    RendererManager = 3
    GameStateManager = 4
    CollisionManager = 5


class EventActionType:
    MainMenuScene = 0
    EarthScene = 1
    MenuCamera = 2
    GameCamera = 3
    PlaySound = 4
    StopSound = 5
    StopAllSounds = 6
    SetSoundVolume = 7
    SetSoundMasterVolume = 8
    ExitGame = 9
    DebugModeOn = 10
    DebugModeOff = 11
    LevelScene = 12
    PauseMenuScene = 13
    MarsScene = 14
    SaturnScene = 15
    SetUITextHelper = 16
    TurnOnTeleporter = 17
    SetUpLevel = 18
    SetCameraTarget = 19
    SetUpColliders = 20
    RemoveCollliderFromQuadTree = 21
    SoundMenuScene = 22
    DeathScene = 23
