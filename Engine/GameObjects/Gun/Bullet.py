from abc import abstractmethod

from App.Constants.Application import Application
from App.Constants.Constants import Constants
from Engine.GameObjects.Components.Component import Component
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Collider import Collider
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.GameObjects.GameObject import GameObject
from Engine.GameObjects.Gun.BulletCollider import BulletCollider
from Engine.GameObjects.Gun.BulletController import BulletController
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.Enums.GameObjectEnums import GameObjectType, GameObjectCategory
from Engine.Other.Enums.RendererLayers import RendererLayers


class Bullet(GameObject):
    def __init__(self, name, material, bullet_damage, bullet_speed, transform=None, game_object_type=GameObjectType.Dynamic, game_object_category=GameObjectCategory.Bullet):
        super().__init__(name, transform, game_object_type, game_object_category)
        self.__bullet_damage = bullet_damage
        self.__bullet_speed = bullet_speed
        self.__material = material

    @property
    def bullet_damage(self):
        return self.__bullet_damage

    def fire(self, direction, color):
        self.__material.color = color
        self.add_component(BoxCollider2D("Bullet Box Collider"))
        self.add_component(Renderer2D("Bullet Renderer", self.__material, RendererLayers.Bullet))
        self.add_component(Rigidbody2D("Bullet Rigidbody"))
        self.add_component(BulletCollider("Bullet Collider"))
        self.add_component(BulletController("Bullet Controller", self.__bullet_speed, direction))
        Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.CollisionManager, EventActionType.AddColliderToQuadTree, [self.get_component(BoxCollider2D)]))

        super().start()

    def clone(self):
        bullet = Bullet(self.name, self.__material.clone(), self.__bullet_damage, self.__bullet_speed, self.transform.clone(), self.game_object_type, self.game_object_category)

        for component in self._components:
            cloned_component = component.clone()
            bullet.add_component(cloned_component)

        return bullet

