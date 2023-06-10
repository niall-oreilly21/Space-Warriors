from pygame import Vector2

from App.Constants.Application import Application
from Engine.GameObjects.Components.Component import Component
from Engine.GameObjects.Components.FollowController import FollowController
from Engine.Graphics.Materials.RectMaterial2D import RectMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D


class HealthBarController(FollowController):
    def __init__(self, name, target):
        super().__init__(name, target)
        self._material = None
        self.__health = None
        self.__initial_width = 0
        self.__current_width = 0

    def start(self):
        for renderer in self._parent.get_components(Renderer2D):
            if isinstance(renderer.material, RectMaterial2D):
                if renderer.name == "Health Bar Renderer Rect":
                    self._material = renderer.material
                    self.__initial_width = self._material.width
                    self.__current_width = self.__initial_width

    def change_colour(self):
        if self.__current_width <= 0.25 * self.__initial_width:
            self._material.color = (255, 0, 0)
        elif self.__current_width <= 0.5 * self.__initial_width:
            self._material.color = (255, 221, 0)

    def update(self, game_time):
        self.__health = self._target.health
        health_percentage = self.__health / self._target.initial_health
        self.__current_width = self.__initial_width * health_percentage
        self._material.width = min(self.__current_width, self.__initial_width)
        self.change_colour()

    def _follow_target(self):
        pass

    def clone(self):
        return HealthBarController(self.name, self.target)
