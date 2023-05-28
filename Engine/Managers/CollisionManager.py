
import math

from pygame import Rect

from App.test1 import CollisionArea
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Collider2D import Collider2D
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Other.Interfaces.IStartable import IStartable
from Engine.Other.Interfaces.IUpdateable import IUpdateable


class CollisionManager(IUpdateable):
    def __init__(self, collision_range, scene_manager, camera_manager):
        self.__collision_range = collision_range
        self.__scene_manager = scene_manager
        self.__camera_manager = camera_manager
        self.collision_area = CollisionArea(self.__camera_manager.active_camera.parent.transform.position.x, self.__camera_manager.active_camera.parent.transform.position.y
                                       , self.__camera_manager.active_camera.viewport.x, self.__camera_manager.active_camera.viewport.y)

    def check_collision(self, collider1, collider2):
        if collider1.collides_with(collider2):
            collider1_entity = collider1.parent
            collider2_entity = collider2.parent

            displacement = collider1.calculate_displacement_vector(collider2)

            # Adjust the colliders' positions by the displacement vector
            collider1_entity.transform.position += displacement

            # Handle the collision response if needed
            collider = collider1.parent.get_component(Collider2D)
            if collider is not None:
                collider.handle_response(collider2_entity)

    def start(self):
        pass

    def update(self, game_time):
        pass

        # Iterate through all colliders or pairs of colliders to check for collisions
        colliders = self.__scene_manager.active_scene.get_all_components_by_type(BoxCollider2D)

        self.collision_area.x = self.__camera_manager.active_camera.parent.transform.position.x
        self.collision_area.y = self.__camera_manager.active_camera.parent.transform.position.y

        colliders_on_screen = []
        for collider in colliders:

            if self.collision_area.intersects_screen(collider.bounds):
                colliders_on_screen.append(collider)

        # Use colliders_on_screen for further processing or collision checks
        for i in range(len(colliders_on_screen)):
            collider1 = colliders_on_screen[i]
            for j in range(i + 1, len(colliders_on_screen)):
                collider2 = colliders_on_screen[j]
                if self.collision_area.is_in_range(collider1.bounds, collider2.bounds, self.__collision_range):
                    self.check_collision(collider1, collider2)


