from typing import Dict

import pygame

from Engine.GameObjects.Components.Camera import Camera
from Engine.GameObjects.GameObject import GameObject
from Engine.Other.Interfaces.IUpdateable import IUpdateable
from Engine.Other.Enums.GameObjectEnums import GameObjectType


class CameraManager(IUpdateable):
    def __init__(self, screen, sceneManager):
        self.__screen = screen
        self.__active_camera = None
        self.__active_game_object = None
        self.__cameras: Dict[str, GameObject] = {}
        self.__needs_redraw = True
        self.__sceneManager = sceneManager
        self.player_is_moving = False

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

    def __set_viewport(self):
        self.__screen = pygame.display.set_mode((self.__active_camera.viewport.x, self.__active_camera.viewport.y))
        self.__needs_redraw = True


    def update(self, game_time):
        self.__active_game_object.update(game_time)

        game_objects = self.__sceneManager.active_scene.find_all_by_type(GameObjectType.Dynamic)


        # Apply the offset to the game objects' positions or rendering


