from pygame import Vector2

from Engine.GameObjects.Components.FollowController import FollowController
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D


class GunController(FollowController):
    def __init__(self, name, target):
        super().__init__(name, target)
        self.__target_box_collider = None

    def start(self):
        self.__target_box_collider = self._target.get_component(BoxCollider2D)
        self.__rb = self._target.get_component(Renderer2D)

    def update(self, game_time):
       self._follow_target()

    def _follow_target(self):
        if self.__target_box_collider:
            #print(self._parent.transform.position)

            #target_position = self.__target_box_collider.bounds.center

            #print(target_position)
            # self._parent.transform.position = Vector2(target_position[0] - self.__rb.material.source_rect.width / 2,
            #                                           target_position[1] - self.__rb.material.source_rect.height / 2)
            self._parent.transform.position = self.target.transform.position


    def clone(self):
        return GunController(self.name, self.target)