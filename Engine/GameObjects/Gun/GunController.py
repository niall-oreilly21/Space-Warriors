from pygame import Vector2

from Engine.GameObjects.Components.FollowController import FollowController
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D


class GunController(FollowController):
    def __init__(self, name, target):
        super().__init__(name, target)
        self.__target_box_collider = None

    def start(self):
        self.__target_box_collider = self._target.get_component(BoxCollider2D)

    def update(self, game_time):
        if self.__target_box_collider:
            target_position = self.__target_box_collider.bounds.center
            #displacement = target_position - self._parent.transform.position
            self._parent.transform.position = Vector2(target_position[0],target_position[1])

    def clone(self):
        return GunController(self.name, self.target)