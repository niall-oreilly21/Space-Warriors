from Engine.Other.Interfaces.IStartable import IStartable
from Engine.Other.Interfaces.IUpdateable import IUpdateable


class SceneManager(IUpdateable, IStartable):
    def __init__(self):
        self.__scenes = {}
        self.__active_scene = None

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
