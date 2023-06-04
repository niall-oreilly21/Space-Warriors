import pygame
import time

from App.Constants.Application import Application
from App.Constants.Constants import Constants
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Managers.Manager import Manager
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType


def load_scene():
    load_time = .4  # Adjust this value as needed
    time.sleep(load_time)


class SceneManager(Manager):
    def __init__(self, event_dispatcher):
        super().__init__(event_dispatcher)
        self.__scenes = {}
        self.__active_scene = None
        self.__event_dispatcher = event_dispatcher

    def _subscribe_to_events(self):
        self._event_dispatcher.add_listener(EventCategoryType.SceneManager, self._handle_events)

    def _handle_events(self, event_data):
        if event_data.event_action_type == EventActionType.MainMenuScene:
            load_scene()
            self.__event_dispatcher.dispatch_event(EventData(EventCategoryType.CameraManager, EventActionType.MenuCamera))
            self.set_active_scene(Constants.Scene.MAIN_MENU)
            Application.ActiveScene = self.__active_scene

        elif event_data.event_action_type == EventActionType.ExitGame:
            pygame.quit()

        elif event_data.event_action_type == EventActionType.EarthScene:
            load_scene()
            self.__event_dispatcher.dispatch_event(
                EventData(EventCategoryType.RendererManager, EventActionType.DebugModeOn))
            self.__event_dispatcher.dispatch_event(EventData(EventCategoryType.CameraManager, EventActionType.GameCamera))
            self.set_active_scene(Constants.Scene.EARTH)
            Application.ActiveScene = self.__active_scene
            Application.CurrentLevel = Constants.Scene.EARTH

        elif event_data.event_action_type == EventActionType.LevelScene:
            load_scene()
            self.__event_dispatcher.dispatch_event(EventData(EventCategoryType.CameraManager, EventActionType.MenuCamera))
            self.set_active_scene(Constants.Scene.LEVEL_MENU)
            Application.ActiveScene = self.__active_scene

        elif event_data.event_action_type == EventActionType.PauseMenuScene:
            self.__event_dispatcher.dispatch_event(EventData(EventCategoryType.CameraManager, EventActionType.MenuCamera))
            self.set_active_scene(Constants.Scene.PAUSE_MENU)
            Application.ActiveScene = self.__active_scene

        elif event_data.event_action_type == EventActionType.MarsScene:
            load_scene()
            self.__event_dispatcher.dispatch_event(
                EventData(EventCategoryType.RendererManager, EventActionType.DebugModeOn))
            self.__event_dispatcher.dispatch_event(EventData(EventCategoryType.CameraManager, EventActionType.GameCamera))
            self.set_active_scene(Constants.Scene.MARS)
            Application.ActiveScene = self.__active_scene
            Application.CurrentLevel = Constants.Scene.MARS

        elif event_data.event_action_type == EventActionType.SaturnScene:
            load_scene()
            self.__event_dispatcher.dispatch_event(
                EventData(EventCategoryType.RendererManager, EventActionType.DebugModeOn))
            self.__event_dispatcher.dispatch_event(EventData(EventCategoryType.CameraManager, EventActionType.GameCamera))
            self.set_active_scene(Constants.Scene.SATURN)
            Application.ActiveScene = self.__active_scene
            Application.CurrentLevel = Constants.Scene.SATURN

        elif event_data.event_action_type == EventActionType.SoundMenuScene:
            self.__event_dispatcher.dispatch_event(EventData(EventCategoryType.CameraManager, EventActionType.MenuCamera))
            self.set_active_scene(Constants.Scene.SOUND_MENU)
            Application.ActiveScene = self.__active_scene
            self.__set_mouse_position()


    @property
    def active_scene(self):
        return self.__active_scene

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
