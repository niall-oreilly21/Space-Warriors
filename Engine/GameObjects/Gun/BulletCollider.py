from App.Constants.Application import Application
from App.Constants.Constants import Constants
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Collider import Collider
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.Enums.GameObjectEnums import GameObjectCategory
from Engine.Other.Interfaces.IDamageable import IDamageable


class BulletCollider(Collider):
    def __init__(self, name):
        super().__init__(name)

    def handle_response(self, colliding_game_object):

        if colliding_game_object.game_object_category is GameObjectCategory.Enemy or colliding_game_object.game_object_category is GameObjectCategory.Bullet:
            return

        if isinstance(colliding_game_object, IDamageable):
            colliding_game_object.damage(self._parent.bullet_damage)

        if Application.ActiveScene.contains(self._parent):
             Application.ActiveScene.remove(self._parent)


    def clone(self):
        return BulletCollider(self.name)