from pygame import Vector2

from App.Components.Controllers.HealthBarController import HealthBarController
from App.Constants.Application import Application
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.Graphics.Materials.RectMaterial2D import RectMaterial2D
from Engine.Graphics.Materials.TextureMaterial2D import TextureMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D

class EnemyHealthBarController(HealthBarController):
    def __init__(self, name, target):
        super().__init__(name, target)
        self.__texture_material = None
        self.__is_active = False

    def start(self):
        super().start()
        self._target_box_collider = self._target.get_component(BoxCollider2D)

        for renderer in self._parent.get_components(Renderer2D):

            if isinstance(renderer.material, TextureMaterial2D):
                self.__texture_material = renderer.material

    def update(self, game_time):
        super().update(game_time)

        if not self.__is_active:
            self.__check_health()

        self._follow_target()

    def __check_health(self):
        if self.target.is_hit():
            self.__is_active = True
            self.__turn_on_renderers()

    def _follow_target(self):
        target_center = self._target_box_collider.bounds.center
        desired_position = Vector2(target_center[0] - self.__texture_material.source_rect.width * self.transform.scale.x / 2,
                                   target_center[1] - self.__texture_material.source_rect.height * self.transform.scale.y * 1.5)


        self.transform.position = desired_position

    def __turn_on_renderers(self):
        for renderer in self._parent.get_components(Renderer2D):
            renderer.is_drawing = True

    def clone(self):
        return EnemyHealthBarController(self.name, self.target)


