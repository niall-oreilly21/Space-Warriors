import math
import time

import pygame
from pygame import Rect, Vector2

from App.Components.Controllers.EnemyController import EnemyController
from App.Components.Controllers.PlayerController import PlayerController
from App.Constants.Application import Application
from Engine.GameObjects.Character import Character
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Collider import Collider
from Engine.GameObjects.Components.Physics.CollisionArea import CollisionArea
from Engine.GameObjects.Components.Physics.Point import Point
from Engine.GameObjects.Components.Physics.QuadTree import QuadTree
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Managers.Manager import Manager
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.Enums.GameObjectEnums import GameObjectType
from Engine.Other.Enums.RendererLayers import RendererLayers
from Engine.Other.Interfaces.IStartable import IStartable
from Engine.Other.Interfaces.IUpdateable import IUpdateable


class CollisionManager(Manager):
    def __init__(self, collision_range, scene_manager, camera_manager, event_dispatcher):
        super().__init__(event_dispatcher)
        self.__colliders = None
        self.__collision_range = collision_range
        self.__scene_manager = scene_manager
        self.__camera_manager = camera_manager
        self.collision_area = CollisionArea(self.__camera_manager.active_camera.parent.transform.position.x,
                                            self.__camera_manager.active_camera.parent.transform.position.y,
                                            self.__camera_manager.active_camera.viewport.x,
                                            self.__camera_manager.active_camera.viewport.y)
        self.colliders = {}
        self.grid_cell_size = 72  # Adjust the cell size based on your colliders and scene size
        self.grid = {}
        self.colliding_cells = {}
        self.quad_tree = QuadTree(self.collision_area.boundary, 4)
        self.dynamic_objects_colliders = []

    def update_collision_area(self):
        camera = self.__camera_manager.active_camera
        viewport = camera.viewport
        camera_position = camera.parent.transform.position

        viewport_center = Vector2(viewport.x / 2, viewport.y / 2)
        target_position = Application.Player.transform.position

        # Adjust x and y coordinates to center around the player
        # x = target_position.x - (self.collision_area.width / 2)
        # y = target_position.y - (self.collision_area.height / 2)

        self.collision_area = CollisionArea(target_position.x - 100, target_position.y - 100, 200, 200)

    def collision_area(self):
        return self.collision_area
    def start(self):
        self.__colliders = self.__scene_manager.active_scene.get_all_components_by_type(BoxCollider2D)
        dynamic_objects = self.__scene_manager.active_scene.find_all_by_type(GameObjectType.Dynamic)

        for object in dynamic_objects:
            self.dynamic_objects_colliders.append(object.get_component(BoxCollider2D))

        self.quad_tree = QuadTree(pygame.Rect(0,0, 110 * 72, 120 * 72), 4)

        print("Colliders: ", len(self.__colliders))

        #print(len(self.__colliders))
        # Insert colliders into the Quadtree
        for collider in self.__colliders:
            # if collider.parent.name == "Teleporter":
            #     print("Teleporter,", collider.bounds)
            self.quad_tree.insert(collider)

        self.quad_tree.print_quadtree()



    def update(self, game_time):
        # Update the collision area based on the camera position
        self.update_collision_area()

        #print(self.collision_area.boundary)

        for collider in self.dynamic_objects_colliders:
            self.quad_tree.remove(collider)

        for collider in self.dynamic_objects_colliders:
            self.quad_tree.insert(collider)

        potential_colliders = list(self.quad_tree.query(self.collision_area.boundary))


        #print("In range collisions", len(potential_colliders))

        # self.quad_tree.print_children()

        # for collider in potential_colliders:
        #     print(collider.parent.name, ", Bounds: ", collider.bounds)
        #
        # print()

        # for i in range(len(self.__colliders)):
        #     collider1 = self.__colliders[i]
        #     for j in range(i + 1, len(self.__colliders)):
        #         collider2 = self.__colliders[j]
        #         self.check_collision(collider1, collider2, game_time)

        for i in range(len(potential_colliders)):
            collider1 = potential_colliders[i]
            for j in range(i + 1, len(potential_colliders)):
                collider2 = potential_colliders[j]
                self.check_collision(collider1, collider2, game_time)


    def _subscribe_to_events(self):
        self._event_dispatcher.add_listener(EventCategoryType.CollisionManager, self._handle_events)

    def _handle_events(self, event_data):
        if event_data.event_action_type == EventActionType.SetUpColliders:
            self.start()

    def add_collider(self, collider):
        # Add a collider to the dictionary using its parent as the key
        self.colliders[collider.parent] = collider

    def remove_collider(self, collider):
        # Remove a collider from the dictionary using its parent as the key
        if collider.parent in self.colliders:
            del self.colliders[collider.parent]

    def check_collision(self, collider1, collider2, game_time):
        # pass
        collider1_entity = collider1.parent
        collider2_entity = collider2.parent

        if collider1_entity == collider2_entity:
            return

        #print(collider1_entity.name)
        #print()

        if collider1.collides_with(collider2):
            print("YES")
            print(collider1_entity.name)
            print(collider2_entity.name)
            if (collider1_entity.name == "Tree" or collider1_entity.name == "LowTree") \
                    and isinstance(collider2_entity, Character):
                collider1_entity.get_component(Renderer2D).layer = RendererLayers.WorldObjects
            elif (collider2_entity.name == "Tree" or collider2_entity.name == "LowTree") \
                    and isinstance(collider1_entity, Character):
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
                    # collider1_rigidbody.velocity = 0
                    pass
                elif is_collider1_static and collider2_rigidbody:
                    # collider2_rigidbody.velocity = Vector2(0, 0)
                    pass

            if collider1_entity.get_component(Collider):
                collider1_entity.get_component(Collider).handle_response(collider2_entity)

            if collider2_entity.get_component(Collider):
                collider2_entity.get_component(Collider).handle_response(collider1_entity)
        else:
            if (collider1_entity.name == "Tree" or collider1_entity.name == "LowTree") \
                    and isinstance(collider2_entity, Character):
                collider1_entity.get_component(Renderer2D).layer = RendererLayers.Tree
            elif (collider2_entity.name == "Tree" or collider2_entity.name == "LowTree") \
                    and isinstance(collider1_entity, Character):
                collider2_entity.get_component(Renderer2D).layer = RendererLayers.Tree

            if collider1_entity.get_component(Collider):
                collider1_entity.get_component(Collider).handle_collision_exit()

            if collider2_entity.get_component(Collider):
                collider2_entity.get_component(Collider).handle_collision_exit()


