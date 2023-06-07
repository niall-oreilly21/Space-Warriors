from pygame import Vector2

from App.Constants.Application import Application
from Engine.GameObjects.Components.Component import Component
from Engine.Graphics.Materials.RectMaterial2D import RectMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D

class HealthBarController(Component):
    def __init__(self, name):
        super().__init__(name)
        self.__material = None
        self.__health = None
        self.__initial_width = 0
        self.__current_width = 0

    def start(self):
        for renderer in self._parent.get_components(Renderer2D):
            if isinstance(renderer.material, RectMaterial2D):
                if renderer.name == "Health Bar Renderer Rect":
                    self.__material = renderer.material
                    self.__initial_width = self.__material.width
                    self.__current_width = self.__initial_width

    def change_colour(self):
        if self.__current_width <= 0.25 * self.__initial_width:
            self.__material.color = (255, 0, 0)

    def update(self, game_time):
        self.__health = Application.Player.health
        health_percentage = self.__health / 100.0
        self.__current_width = (self.__initial_width * health_percentage) / 2
        self.__material.width = self.__current_width
        self.change_colour()
