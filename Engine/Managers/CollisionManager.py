import math

import pygame
from pygame import Rect

from App.Components.Controllers.EnemyController import EnemyController
from App.Components.Controllers.PlayerController import PlayerController
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Collider2D import Collider2D
from Engine.GameObjects.Components.Physics.CollisionArea import CollisionArea
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Other.Interfaces.IStartable import IStartable
from Engine.Other.Interfaces.IUpdateable import IUpdateable


class CollisionManager(IUpdateable):
    def __init__(self, collision_range, scene_manager, camera_manager):
        self.__collision_range = 200
        self.__scene_manager = scene_manager
        self.__camera_manager = camera_manager
        self.collision_area = CollisionArea(self.__camera_manager.active_camera.parent.transform.position.x,
                                            self.__camera_manager.active_camera.parent.transform.position.y,
                                            self.__camera_manager.active_camera.viewport.x,
                                            self.__camera_manager.active_camera.viewport.y)

    def check_collision(self, collider1, collider2, game_time):
        if collider1.collides_with(collider2):
            collider1_entity = collider1.parent
            collider2_entity = collider2.parent

            collider1_rigidbody = collider1_entity.get_component(Rigidbody2D)
            collider2_rigidbody = collider2_entity.get_component(Rigidbody2D)


            is_collider1_static = collider1_entity.game_object_type.Static
            is_collider2_static = collider2_entity.game_object_type.Static

            displacement = collider1.calculate_displacement_vector(collider2)

            if displacement.length_squared() != 0:  # Check for non-zero length
                if collider1_rigidbody and collider2_rigidbody:
                    total_mass = collider1_rigidbody.mass + collider2_rigidbody.mass

                    # Calculate the relative velocity between the colliders
                    relative_velocity = collider2_rigidbody.velocity - collider1_rigidbody.velocity

                    # Calculate the impulse
                    impulse = (-(1 + 0.4) * relative_velocity.dot(displacement)) / (
                            displacement.length_squared() * (
                            1 / collider1_rigidbody.mass + 1 / collider2_rigidbody.mass)
                    )

                    # Adjust the impulse magnitude for a smoother result
                    impulse *= 35  # Adjust this factor as needed

                    # Apply the impulse to the velocities if the relative velocity is below a threshold
                    velocity_threshold = 0.6  # Adjust this threshold as needed
                    if relative_velocity.length() < velocity_threshold:
                        collider1_rigidbody.velocity -= impulse * (
                                displacement / displacement.length()) / collider1_rigidbody.mass
                        collider2_rigidbody.velocity += impulse * (
                                displacement / displacement.length()) / collider2_rigidbody.mass

                elif collider1_rigidbody and is_collider2_static:

                    # Handle collision with a static object
                    collision_normal = displacement.normalize()

                    relative_velocity = collider2_rigidbody.velocity

                    impulse_magnitude = (-(1 + 20) * relative_velocity.dot(collision_normal))

                    impulse_vector = impulse_magnitude * collision_normal

                    impulse_vector *= 90

                    collider1_rigidbody.velocity += impulse_vector


                elif is_collider1_static and collider2_rigidbody:
                    # Handle collision with a static object
                    collision_normal = displacement.normalize()
                    relative_velocity = collider2_rigidbody.velocity
                    impulse_magnitude = (-(1 + 0.8) * relative_velocity.dot(collision_normal))
                    impulse_vector = impulse_magnitude * collision_normal
                    impulse_vector *= 20

                    collider2_rigidbody.velocity += impulse_vector


                if collider1_entity.get_component(Collider2D):
                    collider1_entity.get_component(Collider2D).handle_response(collider2_entity)


    def start(self):
        pass

    def update(self, game_time):
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
                    self.check_collision(collider1, collider2, game_time)
