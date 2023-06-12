import time

import pygame

from App.Constants.Application import Application
from App.Constants.GameConstants import GameConstants
from Engine.GameObjects.Components.Cameras.ThirdPersonController import ThirdPersonController
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.Managers import SceneManager
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType


class ButtonCollider2D(BoxCollider2D):
    def __init__(self, name, anchor=pygame.Vector2(0, 0)):
        super().__init__(name, anchor)
        self._mouse_position = None

    def start(self):
        super().start()

    def update(self, game_time):
        self._mouse_position = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        if self.bounds.collidepoint(self._mouse_position) and mouse_buttons[0]:
            self.button_pressed()

    def draw(self, screen, camera_position):
        super().draw(screen, camera_position)

    def button_pressed(self):
        self.__load_event()
        GameConstants.EVENT_DISPATCHER.dispatch_event(
            EventData(EventCategoryType.SoundManager, EventActionType.PlaySound, [GameConstants.Music.BUTTON_SOUND, False]))
        if self._parent.name == GameConstants.Button.START_BUTTON:
            GameConstants.EVENT_DISPATCHER.dispatch_event(
                EventData(EventCategoryType.SceneManager, EventActionType.CharacterSelectionMenuScene))
        elif self._parent.name == GameConstants.Button.QUIT_BUTTON:
            GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                    EventActionType.ExitGame))
        elif self._parent.name == GameConstants.Button.RESUME_BUTTON:
            GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager, EventActionType.SetToLastActiveScene))

        if self._parent.name == GameConstants.Button.MAIN_MENU_BUTTON:
            GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                    EventActionType.MainMenuScene))
        elif self._parent.name == GameConstants.Button.SOUND_BUTTON:
            GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                    EventActionType.SoundMenuScene))
        elif self._parent.name == GameConstants.Button.MUTE_BUTTON:
            GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SoundManager,
                                                                    EventActionType.SetSoundMasterVolume, [0]))
        elif self._parent.name == GameConstants.Button.UNMUTE_BUTTON:
            GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SoundManager,
                                                                    EventActionType.SetSoundMasterVolume, [0.5]))
        elif self._parent.name == GameConstants.Button.EARTH_BUTTON:
            GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                    EventActionType.EarthScene))
        elif self._parent.name == GameConstants.Button.MARS_BUTTON:
            GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                    EventActionType.MarsScene))
        elif self._parent.name == GameConstants.Button.SATURN_BUTTON:
            GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                    EventActionType.SaturnScene))
        elif self._parent.name == GameConstants.Button.RESTART_BUTTON:
            GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                    EventActionType.ResetLevelScene))
        elif self._parent.name == GameConstants.Button.GIRL_PLAYER_BUTTON:
            GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                    EventActionType.GirlCharacterSelected))
        elif self._parent.name == GameConstants.Button.BOY_PLAYER_BUTTON:
            GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                    EventActionType.BoyCharacterSelected))
        elif self._parent.name == GameConstants.Button.CONTROLS_BUTTON:
            GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                    EventActionType.ControlsMenuScene))
        elif self._parent.name == GameConstants.Button.BACK_BUTTON:
            GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                    EventActionType.MainMenuScene))
        elif self._parent.name == GameConstants.Button.LEVELS_BUTTON:
            GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                    EventActionType.LevelScene))

    def __load_event(self):
        load_time = .4
        time.sleep(load_time)

    def clone(self):
        return ButtonCollider2D(self._name)
