from typing import Dict

import pygame

from Engine.GameObjects.Components.Cameras.Camera import Camera
from Engine.GameObjects.GameObject import GameObject
from Engine.Managers.Manager import Manager
from Engine.Other.Enums.EventEnums import EventCategoryType
from Engine.Other.Interfaces.IStartable import IStartable
from Engine.Other.Interfaces.IUpdateable import IUpdateable
from Engine.Other.Enums.GameObjectEnums import GameObjectType


class CameraManager(Manager):
    def __init__(self, screen, sceneManager, event_dispatcher):
        super().__init__(event_dispatcher)
        self.__screen = screen
        self.__active_camera = None
        self.__active_game_object = None
        self.__cameras: Dict[str, GameObject] = {}
        self.__needs_redraw = True
        self.__sceneManager = sceneManager
        self.player_is_moving = False

    def _subscribe_to_events(self):
        self._event_dispatcher.add_listener(EventCategoryType.CameraManager, self._handle_events)

    def _handle_events(self, event_data):
        pass


    @property
    def active_camera_transform(self):
        if self.__active_game_object is None:
            raise ValueError("ActiveCamera not set! Call SetActiveCamera()")
        return self.__active_game_object.transform

    @property
    def active_camera_name(self):
        if self.__active_game_object is None:
            raise ValueError("ActiveCamera not set! Call SetActiveCamera()")
        return self.__active_game_object.name

    @property
    def active_camera(self):
        if self.__active_camera is None:
            raise ValueError("ActiveCamera not set! Call SetActiveCamera()")
        return self.__active_camera

    def add(self, camera):
        id = camera.name.strip().lower()

        if id in self.__cameras:
            return False

        self.__cameras[id] = camera
        return True

    def set_active_camera(self, id):
        camera_game_object = None
        id = id.strip().lower()

        if id in self.__cameras:
            camera_game_object = self.__cameras[id]

        if camera_game_object is not None:
            self.__active_camera = camera_game_object.get_component(Camera)
            self.__active_game_object = camera_game_object

        if self.__active_camera:
            self.__set_viewport()

    def get_active_camera_position(self):
        return self.__active_camera.parent.position

    def __set_viewport(self):
        self.__screen = pygame.display.set_mode((self.__active_camera.viewport.x, self.__active_camera.viewport.y))
        self.__needs_redraw = True

    def start(self):
        self.__active_game_object.start()

    def update(self, game_time):
        self.__active_game_object.update(game_time)
