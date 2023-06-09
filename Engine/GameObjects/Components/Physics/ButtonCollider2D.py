import time

import pygame

from App.Constants.Application import Application
from App.Constants.Constants import Constants
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
        Constants.EVENT_DISPATCHER.dispatch_event(
            EventData(EventCategoryType.SoundManager, EventActionType.PlaySound, [Constants.Music.BUTTON_SOUND, False]))
        if self._parent.name == Constants.Button.START_BUTTON:
            Constants.EVENT_DISPATCHER.dispatch_event(
                EventData(EventCategoryType.SceneManager, EventActionType.LevelScene))
        elif self._parent.name == Constants.Button.QUIT_BUTTON:
            Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                EventActionType.ExitGame))
        elif self._parent.name == Constants.Button.RESUME_BUTTON:
            Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager, EventActionType.SetToLastActiveScene))

        if self._parent.name == Constants.Button.MAIN_MENU_BUTTON:
            Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                EventActionType.MainMenuScene))
        elif self._parent.name == Constants.Button.SOUND_BUTTON:
            Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                EventActionType.SoundMenuScene))
        elif self._parent.name == Constants.Button.MUTE_BUTTON:
            Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SoundManager,
                                                                EventActionType.SetSoundMasterVolume, [0]))
        elif self._parent.name == Constants.Button.UNMUTE_BUTTON:
            Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SoundManager,
                                                                EventActionType.SetSoundMasterVolume, [0.5]))
        elif self._parent.name == Constants.Button.EARTH_BUTTON:
            Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                EventActionType.EarthScene))
        elif self._parent.name == Constants.Button.MARS_BUTTON:
            Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                EventActionType.MarsScene))
        elif self._parent.name == Constants.Button.SATURN_BUTTON:
            Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                EventActionType.SaturnScene))
        elif self._parent.name == Constants.Button.RESTART_BUTTON:
                print("HERE")
                Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,EventActionType.ResetLevelScene))

    def __load_event(self):
        load_time = .4
        time.sleep(load_time)

    def clone(self):
        return ButtonCollider2D(self._name)
