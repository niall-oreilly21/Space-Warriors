from App.Constants.Application import Application
from App.Constants.Constants import Constants
from Engine.GameObjects.Components.Component import Component
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType


class BulletController(Component):
    def __init__(self, name, bullet_speed, direction, bullet_rotation_speed = 2, bullet_span_life = 5):
        super().__init__(name)
        self.__bullet_speed = bullet_speed / 10000
        self.__direction = direction
        self.__bullet_rotation_speed = bullet_rotation_speed
        self.__rb = None
        self.__bullet_span_life = bullet_span_life * 1000
        self.__total_elapsed_time = 0

    def start(self):
        Constants.EVENT_DISPATCHER.dispatch_event(
            EventData(EventCategoryType.SoundManager, EventActionType.PlaySound,
                      [Constants.Music.BULLET_SOUND, None]))
        self.__rb = self._parent.get_component(Rigidbody2D)

    def update(self, game_time):
        self.transform.rotation = 0.1 * game_time.elapsed_time

        if self.transform.rotation >= 360:
            self.transform.rotation = 0
        self.__rb.velocity = self.__direction * self.__bullet_speed

        self.__total_elapsed_time += game_time.elapsed_time

        if self.__total_elapsed_time >= self.__bullet_span_life:
            self.__remove_bullet()

    def __remove_bullet(self):
        Application.ActiveScene.remove(self._parent)

    def clone(self):
        return BulletController(self.name, self.__bullet_speed, self.__direction, self.__bullet_rotation_speed)