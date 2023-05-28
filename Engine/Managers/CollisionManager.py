import math

from pygame import Rect

from App.Components.Colliders.AttackBoxCollider2D import AttackBoxCollider2D
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Collider2D import Collider2D
from Engine.GameObjects.Components.Physics.CollisionArea import CollisionArea
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Other.Interfaces.IStartable import IStartable
from Engine.Other.Interfaces.IUpdateable import IUpdateable


def check_collision(collider1, collider2):

    if collider1.collides_with(collider2):
        collider1_entity = collider1.parent
        collider2_entity = collider2.parent
        if not isinstance(collider1, AttackBoxCollider2D):

            overlap_x = min(collider1.bounds.right - collider2.bounds.left,
                            collider2.bounds.right - collider1.bounds.left)
            overlap_y = min(collider1.bounds.bottom - collider2.bounds.top,
                            collider2.bounds.bottom - collider1.bounds.top)

            if overlap_x < overlap_y:
                if overlap_x == collider1.bounds.right - collider2.bounds.left:
                    # Check if it's a corner collision
                    if collider1.bounds.bottom == collider2.bounds.top:
                        collider1_entity.transform.position.x = collider2.bounds.left - collider1.bounds.width
                        collider1_entity.transform.position.y = collider2.bounds.top - collider1.bounds.height
                    else:
                        collider1_entity.transform.position.x -= overlap_x
                else:
                    # Check if it's a corner collision
                    if collider1.bounds.bottom == collider2.bounds.top:
                        collider1_entity.transform.position.x = collider2.bounds.right
                        collider1_entity.transform.position.y = collider2.bounds.top - collider1.bounds.height
                    else:
                        collider1_entity.transform.position.x += overlap_x
            else:
                if overlap_y == collider1.bounds.bottom - collider2.bounds.top:
                    # Check if it's a corner collision
                    if collider1.bounds.right == collider2.bounds.left:
                        collider1_entity.transform.position.y = collider2.bounds.top - collider1.bounds.height
                        collider1_entity.transform.position.x = collider2.bounds.left - collider1.bounds.width
                    else:
                        collider1_entity.transform.position.y -= overlap_y
                else:
                    # Check if it's a corner collision
                    if collider1.bounds.right == collider2.bounds.left:
                        collider1_entity.transform.position.y = collider2.bounds.bottom
                        collider1_entity.transform.position.x = collider2.bounds.left - collider1.bounds.width
                    else:
                        collider1_entity.transform.position.y += overlap_y

        # Handle the collision response if needed
        collider = collider1.parent.get_component(Collider2D)
        if collider is not None:
            collider.handle_response(collider2_entity)


class CollisionManager(IUpdateable):
    def __init__(self, collision_range, scene_manager, camera_manager):
        self.__collision_range = collision_range
        self.__scene_manager = scene_manager
        self.__camera_manager = camera_manager
        self.collision_area = CollisionArea(self.__camera_manager.active_camera.parent.transform.position.x,
                                            self.__camera_manager.active_camera.parent.transform.position.y,
                                            self.__camera_manager.active_camera.viewport.x,
                                            self.__camera_manager.active_camera.viewport.y)

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
                    check_collision(collider1, collider2)
