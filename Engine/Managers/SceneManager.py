import sys

import pygame
import time

from App.Constants.Application import Application
from App.Constants.Constants import Constants
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Managers.Manager import Manager
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType

class SceneManager(Manager):
    def __init__(self, event_dispatcher):
        super().__init__(event_dispatcher)
        self.__scenes = {}
        self.__active_scene = None

    def _subscribe_to_events(self):
        self._event_dispatcher.add_listener(EventCategoryType.SceneManager, self._handle_events)

    def _handle_events(self, event_data):
        if event_data.event_action_type == EventActionType.MainMenuScene:
            self.__set_menu_scene(Constants.Scene.MAIN_MENU)

        elif event_data.event_action_type == EventActionType.ExitGame:
            pygame.quit()
            sys.exit()

        elif event_data.event_action_type == EventActionType.EarthScene:
            self._event_dispatcher.dispatch_event(EventData(EventCategoryType.RendererManager, EventActionType.DebugModeOn))
            self.set_active_scene(Constants.Scene.EARTH)
            Application.ActiveScene = self.__active_scene
            self._event_dispatcher.dispatch_event(EventData(EventCategoryType.GameStateManager, EventActionType.SetUpLevel))
            Application.CurrentLevel = Constants.Scene.EARTH

        elif event_data.event_action_type == EventActionType.LevelScene:
            self.__set_menu_scene(Constants.Scene.LEVEL_MENU)

        elif event_data.event_action_type == EventActionType.PauseMenuScene:
            self.__dispatch_menu_events()
            Application.LastActiveScene = self.__active_scene
            self.__set_menu_scene(Constants.Scene.PAUSE_MENU)

        elif event_data.event_action_type == EventActionType.DeathScene:
            self.__dispatch_menu_events()
            self.__set_menu_scene(Constants.Scene.DEATH_MENU)

        elif event_data.event_action_type == EventActionType.MarsScene:
            self._event_dispatcher.dispatch_event(EventData(EventCategoryType.RendererManager, EventActionType.DebugModeOn))
            self.set_active_scene(Constants.Scene.MARS)
            Application.ActiveScene = self.__active_scene
            Application.CurrentLevel = Constants.Scene.MARS
            self._event_dispatcher.dispatch_event(EventData(EventCategoryType.GameStateManager, EventActionType.SetUpLevel))

        elif event_data.event_action_type == EventActionType.SaturnScene:
            self._event_dispatcher.dispatch_event(EventData(EventCategoryType.RendererManager, EventActionType.DebugModeOn))
            self.set_active_scene(Constants.Scene.SATURN)
            Application.ActiveScene = self.__active_scene
            Application.CurrentLevel = Constants.Scene.SATURN
            self._event_dispatcher.dispatch_event(EventData(EventCategoryType.GameStateManager, EventActionType.SetUpLevel))

        elif event_data.event_action_type == EventActionType.SoundMenuScene:
            self.__set_menu_scene(Constants.Scene.SOUND_MENU)

        elif event_data.event_action_type == EventActionType.SetToLastActiveScene:
            self.__set_scenes()
            if self.__check_level_scene():
                Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.GameStateManager, EventActionType.LoadLevel))

        elif event_data.event_action_type == EventActionType.ResetLevelScene:
            self.__set_scenes()
            self.set_active_scene(Constants.Scene.EARTH)
            Application.ActiveScene = self.__active_scene
            Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.GameStateManager, EventActionType.SetUpLevel))
            if self.__check_level_scene():
                pass


    @property
    def active_scene(self):
        return self.__active_scene

    def __dispatch_menu_events(self):
        self._event_dispatcher.dispatch_event(EventData(EventCategoryType.CameraManager, EventActionType.MenuCamera))
        self._event_dispatcher.dispatch_event(
            EventData(EventCategoryType.CollisionManager, EventActionType.TurnOffCollisionDetection))

    def __set_scenes(self):
        Application.ActiveScene = Application.LastActiveScene
        Application.LastActiveScene = self.__active_scene
        self.set_active_scene(Application.ActiveScene.name)

    def __set_menu_scene(self, next_scene_name):
            self._event_dispatcher.dispatch_event(EventData(EventCategoryType.CameraManager, EventActionType.MenuCamera))
            self.set_active_scene(next_scene_name)
            Application.ActiveScene = self.__active_scene

    def __check_level_scene(self):
        return self.__active_scene.name is Constants.Scene.EARTH or\
        self.__active_scene.name == Constants.Scene.MARS or\
        self.__active_scene.name == Constants.Scene.SATURN

    def set_active_scene(self, name):
        name = name.strip().lower()
        if name in self.__scenes:
            self.__active_scene = self.__scenes[name]
        return self.__active_scene

    def add(self, name, scene):
        name = name.strip().lower()
        if name in self.__scenes:
            return False
        self.__scenes[name] = scene
        return True

    def update(self, game_time):

        if self.__active_scene is not None:
            self.__active_scene.update(game_time)

    def start(self):
        for active_scene in self.__scenes:
            self.__scenes[active_scene].start()
