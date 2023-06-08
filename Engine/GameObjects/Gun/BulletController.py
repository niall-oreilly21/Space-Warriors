from Engine.GameObjects.Components.Component import Component
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D


class BulletController(Component):
    def __init__(self, name, bullet_speed, direction, bullet_rotation_speed = 20):
        super().__init__(name)
        self.__bullet_speed = bullet_speed
        self.__direction = direction
        self.__bullet_rotation_speed = bullet_rotation_speed
        self.__rb = None

    def start(self):
        self.__rb = self._parent.get_component(Rigidbody2D)

    def update(self, game_time):
        self.__rb.velocity = self.__direction * self.__bullet_speed * 0.001

    def clone(self):
        return BulletController(self.name, self.__bullet_speed, self.__direction, self.__bullet_rotation_speed)