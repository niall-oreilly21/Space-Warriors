import math

import pygame
from pygame import Rect

from App.Components.Colliders.TreeBoxCollider2D import TreeBoxCollider2D
from App.Components.Controllers.EnemyController import EnemyController
from App.Components.Controllers.PlayerController import PlayerController
from Engine.GameObjects.Character import Character
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Collider import Collider
from Engine.GameObjects.Components.Physics.CollisionArea import CollisionArea
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Managers.Manager import Manager
from Engine.Other.Enums.RendererLayers import RendererLayers
from Engine.Other.Interfaces.IStartable import IStartable
from Engine.Other.Interfaces.IUpdateable import IUpdateable


class CollisionManager(Manager):
    def __init__(self, collision_range, scene_manager, camera_manager, event_dispatcher):
        super().__init__(event_dispatcher)
        self.__collision_range = collision_range
        self.__scene_manager = scene_manager
        self.__camera_manager = camera_manager
        self.collision_area = CollisionArea(self.__camera_manager.active_camera.parent.transform.position.x,
                                            self.__camera_manager.active_camera.parent.transform.position.y,
                                            self.__camera_manager.active_camera.viewport.x,
                                            self.__camera_manager.active_camera.viewport.y)

    def _subscribe_to_events(self):
        pass

    def _handle_events(self, event_data):
        pass

    def check_collision(self, collider1, collider2, game_time):
        # pass
        collider1_entity = collider1.parent
        collider2_entity = collider2.parent
        if collider1.collides_with(collider2):
            if isinstance(collider1, TreeBoxCollider2D) and isinstance(collider2_entity, Character):
                collider1_entity.get_component(Renderer2D).layer = RendererLayers.WorldObjects
            elif isinstance(collider2, TreeBoxCollider2D) and isinstance(collider1_entity, Character):
                collider2_entity.get_component(Renderer2D).layer = RendererLayers.WorldObjects

            collider1_rigidbody = collider1_entity.get_component(Rigidbody2D)
            collider2_rigidbody = collider2_entity.get_component(Rigidbody2D)

            is_collider1_static = collider1_entity.game_object_type.Static
            is_collider2_static = collider2_entity.game_object_type.Static

            displacement = collider1.calculate_displacement_vector(collider2)

            if displacement.length_squared() != 0:  # Check for non-zero length
                if collider1_rigidbody and collider2_rigidbody:
                    pass
                elif collider1_rigidbody and is_collider2_static:
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

                elif is_collider1_static and collider2_rigidbody:
                    overlap_x = min(collider2.bounds.right - collider1.bounds.left,
                                    collider1.bounds.right - collider2.bounds.left)
                    overlap_y = min(collider2.bounds.bottom - collider1.bounds.top,
                                    collider1.bounds.bottom - collider2.bounds.top)

                    if overlap_x < overlap_y:
                        if overlap_x == collider2.bounds.right - collider1.bounds.left:
                            # Check if it's a corner collision
                            if collider2.bounds.bottom == collider1.bounds.top:
                                collider2_entity.transform.position.x = collider1.bounds.left - collider2.bounds.width
                                collider2_entity.transform.position.y = collider1.bounds.top - collider2.bounds.height
                            else:
                                collider2_entity.transform.position.x -= overlap_x
                        else:
                            # Check if it's a corner collision
                            if collider2.bounds.bottom == collider1.bounds.top:
                                collider2_entity.transform.position.x = collider1.bounds.right
                                collider2_entity.transform.position.y = collider1.bounds.top - collider2.bounds.height
                            else:
                                collider2_entity.transform.position.x += overlap_x
                    else:
                        if overlap_y == collider2.bounds.bottom - collider1.bounds.top:
                            # Check if it's a corner collision
                            if collider2.bounds.right == collider1.bounds.left:
                                collider2_entity.transform.position.y = collider1.bounds.top - collider2.bounds.height
                                collider2_entity.transform.position.x = collider1.bounds.left - collider2.bounds.width
                            else:
                                collider2_entity.transform.position.y -= overlap_y
                        else:
                            # Check if it's a corner collision
                            if collider2.bounds.right == collider1.bounds.left:
                                collider2_entity.transform.position.y = collider1.bounds.bottom
                                collider2_entity.transform.position.x = collider1.bounds.left - collider2.bounds.width
                            else:
                                collider2_entity.transform.position.y += overlap_y

            if collider1_entity.get_component(Collider):
                collider1_entity.get_component(Collider).handle_response(collider2_entity)
        else:
            if isinstance(collider1, TreeBoxCollider2D) and isinstance(collider2_entity, Character):
                collider1_entity.get_component(Renderer2D).layer = RendererLayers.Tree
            elif isinstance(collider2, TreeBoxCollider2D) and isinstance(collider1_entity, Character):
                collider2_entity.get_component(Renderer2D).layer = RendererLayers.Tree

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
