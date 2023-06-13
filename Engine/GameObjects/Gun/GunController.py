from pygame import Vector2

from Engine.GameObjects.Components.FollowController import FollowController
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D


class GunController(FollowController):
    def __init__(self, name, target):
        super().__init__(name, target)
        self.__target_box_collider = None

    def update(self, game_time):
       self._follow_target()

    def _follow_target(self):
        self._parent.transform.position = self.target.transform.position


    def clone(self):
        return GunController(self.name, self.target)