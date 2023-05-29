from Engine.Managers.EventSystem.EventData import EventData
from Engine.Managers.Manager import Manager
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.Interfaces.IStartable import IStartable
from Engine.Other.Interfaces.IUpdateable import IUpdateable


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
            self.set_active_scene("Main Menu")
            self.__event_dispatcher.dispatch_event(EventData(EventCategoryType.CameraManager, EventActionType.MenuCamera, None))

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
        if  self.__active_scene is not None:
            self.__active_scene.update(game_time)

    def start(self):
        self.__active_scene.start()
