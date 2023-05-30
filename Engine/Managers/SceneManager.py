import pygame

from App.Constants.Constants import Constants
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Managers.Manager import Manager
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType


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
            self.set_active_scene(Constants.Scene.MAIN_MENU)
            self.__event_dispatcher.dispatch_event(
                EventData(EventCategoryType.CameraManager, EventActionType.MenuCamera))
        elif event_data.event_action_type == EventActionType.ExitGame:
            pygame.quit()
        elif event_data.event_action_type == EventActionType.GameScene:
            self.set_active_scene(Constants.Scene.GAME)
            self.__event_dispatcher.dispatch_event(
                EventData(EventCategoryType.CameraManager, EventActionType.GameCamera))
        elif event_data.event_action_type == EventActionType.LevelScene:
            self.set_active_scene(Constants.Scene.LEVEL_MENU)
            self.__event_dispatcher.dispatch_event(
                EventData(EventCategoryType.CameraManager, EventActionType.MenuCamera))

    @property
    def active_scene(self):
        return self.__active_scene

    def set_active_scene(self, id):
        id = id.strip().lower()
        if id in self.__scenes:
            self.__active_scene = self.__scenes[id]
        return self.__active_scene

    def add(self, id, scene):
        id = id.strip().lower()
        if id in self.__scenes:
            return False
        self.__scenes[id] = scene
        return True

    def update(self, game_time):
        if self.__active_scene is not None:
            self.__active_scene.update(game_time)

    def start(self):
        for active_scene in self.__scenes:
            self.__scenes[active_scene].start()
