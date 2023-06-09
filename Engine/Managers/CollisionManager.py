import time

import pygame
from App.Constants.Application import Application
from Engine.GameObjects.Character import Character
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Collider import Collider
from Engine.GameObjects.Components.Physics.CollisionRange import CollisionRange
from Engine.GameObjects.Components.Physics.QuadTree import QuadTree
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Managers.Manager import Manager
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.Enums.GameObjectEnums import GameObjectType, GameObjectCategory
from Engine.Other.Enums.RendererLayers import RendererLayers


class CollisionManager(Manager):
    def __init__(self, map_dimensions, collision_range_target, collision_range_width, collision_range_height, quad_tree_capacity, event_dispatcher):
        super().__init__(event_dispatcher)
        self.__map_dimensions = map_dimensions
        self.__quad_tree_capacity = quad_tree_capacity
        self.__collision_range = CollisionRange(0, 0, collision_range_width, collision_range_height)
        self.__dynamic_objects_colliders = []
        self.__collision_range_target = collision_range_target
        self.__collision_range_target_box_collider = None
        self.__colliders = None
        self.__quad_tree = None
        self.__update = False

    def _subscribe_to_events(self):
        self._event_dispatcher.add_listener(EventCategoryType.CollisionManager, self._handle_events)

    def _handle_events(self, event_data):
        if event_data.event_action_type == EventActionType.SetUpColliders:
            self.start()

        elif event_data.event_action_type == EventActionType.RemoveCollliderFromQuadTree:
            box_collider = event_data.parameters[0]
            self.__remove_box_collider(box_collider)

        elif event_data.event_action_type == EventActionType.AddColliderToQuadTree:
            box_collider = event_data.parameters[0]
            self.__add_box_collider(box_collider)

        elif event_data.event_action_type == EventActionType.DrawCollisionRange:
            screen = event_data.parameters[0]
            camera_position = event_data.parameters[1]
            if self.__update:
                self.__collision_range.draw(screen, camera_position)

        elif event_data.event_action_type == EventActionType.TurnOffCollisionDetection:
            self.__update = False

        elif event_data.event_action_type == EventActionType.TurnOnCollisionDetection:
            self.__update = True

    @property
    def collision_range(self):
        return self.__collision_range


    def __add_box_collider(self, box_collider):
        if box_collider.parent.game_object_type is GameObjectType.Dynamic:
            self.__dynamic_objects_colliders.append(box_collider)
            self.__quad_tree.insert(box_collider)

    def __remove_box_collider(self, box_collider):
        if box_collider.parent.game_object_type is GameObjectType.Dynamic:
            self.__dynamic_objects_colliders.remove(box_collider)
            self.__quad_tree.remove(box_collider)


    def start(self):
        self.__colliders = Application.ActiveScene.get_all_components_by_type(BoxCollider2D)

        self.__set_up_dynamic_game_objects_list()
        self.__set_up_quad_tree()

        self.__collision_range_target_box_collider = self.__collision_range_target.get_component(BoxCollider2D)


    def __set_up_quad_tree(self):
        self.__quad_tree = QuadTree(self.__map_dimensions, self.__quad_tree_capacity)

        for collider in self.__colliders:
            self.__quad_tree.insert(collider)

    def __set_up_dynamic_game_objects_list(self):
        dynamic_game_objects = Application.ActiveScene.find_all_by_type(GameObjectType.Dynamic)

        for game_object in dynamic_game_objects:
            if game_object.get_component(BoxCollider2D):
                self.__dynamic_objects_colliders.append(game_object.get_component(BoxCollider2D))


    def __update_collision_range(self):
        self.__collision_range.x = self.__collision_range_target_box_collider.bounds.centerx - self.__collision_range.width / 2
        self.__collision_range.y = self.__collision_range_target_box_collider.bounds.centery - self.__collision_range.height / 2

    def update(self, game_time):
        if self.__update:
            self.__update_collision_range()
            self.__update_dynamic_game_objects_box_colliders_in_quad_tree()


            potential_colliders = self.__quad_tree.query(self.__collision_range.bounds)

            for i in range(len(potential_colliders)):
                box_collider_one = potential_colliders[i]
                for j in range(i + 1, len(potential_colliders)):
                    box_collider_two = potential_colliders[j]
                    self.__check_collision(box_collider_one, box_collider_two)


    def __update_dynamic_game_objects_box_colliders_in_quad_tree(self):
        for collider in self.__dynamic_objects_colliders:
            self.__quad_tree.remove(collider)
            self.__quad_tree.insert(collider)

    def __change_collision_layers_for_trees(self, collider_one_entity, collider_two_entity, renderer_layer):
        if (collider_one_entity.name == "Tree" or collider_one_entity.name == "LowTree") and isinstance(
                collider_two_entity, Character):
            collider_one_entity.get_component(Renderer2D).layer = renderer_layer

        elif (collider_two_entity.name == "Tree" or collider_two_entity.name == "LowTree") and isinstance(
                collider_one_entity, Character):
            collider_two_entity.get_component(Renderer2D).layer = renderer_layer

    def __handle_collision_responses(self, collider_one, collider_two, collider_one_entity, collider_two_entity):
        if collider_one:
            collider_one.handle_response(collider_two_entity)

        if collider_two:
            collider_two.handle_response(collider_one_entity)

    def __handle_collision_exits(self, collider_one, collider_two):
        if collider_one:
            collider_one.handle_collision_exit()

        if collider_two:
            collider_two.handle_collision_exit()

    def __ignore_physics_collisions(self, collider_one_entity, collider_two_entity):
        return collider_one_entity.game_object_category is GameObjectCategory.Teleporter or collider_two_entity.game_object_category is GameObjectCategory.Teleporter \
        or collider_one_entity.game_object_category is GameObjectCategory.PowerUp or collider_two_entity.game_object_category is GameObjectCategory.PowerUp


    def __handle_collision_physics(self, collider_one_entity, collider_two_entity):
        collider_one_rigidbody = collider_one_entity.get_component(Rigidbody2D)
        collider_two_rigidbody = collider_two_entity.get_component(Rigidbody2D)

        is_collider1_static = collider_one_entity.game_object_type.Static
        is_collider2_static = collider_two_entity.game_object_type.Static

        if self.__ignore_physics_collisions(collider_one_entity, collider_two_entity):
            return

        if collider_one_rigidbody and collider_two_rigidbody:
            pass

        elif collider_one_rigidbody and is_collider2_static:
            collider_one_rigidbody.stop_moving()

            self.calculate_offset(collider_one_entity, collider_two_entity)

        elif is_collider1_static and collider_two_rigidbody:
            collider_two_rigidbody.stop_moving()
            self.calculate_offset(collider_two_entity, collider_one_entity)

    def calculate_offset(self, collider_one_entity_dynamic, collider_two_entity_static):
        rect_one = collider_one_entity_dynamic.get_component(BoxCollider2D).bounds
        rect_two = collider_two_entity_static.get_component(BoxCollider2D).bounds

        # Determine the direction of the collision
        dx = (rect_one.centerx - rect_two.centerx) / (rect_two.width / 2)
        dy = (rect_one.centery - rect_two.centery) / (rect_two.height / 2)

        if abs(dx) > abs(dy):
            # Horizontal collision
            if dx > 0:
                collider_one_entity_dynamic.transform.position.x = rect_two.right
            else:
                collider_one_entity_dynamic.transform.position.x = rect_two.left - rect_one.width
        else:
            # Vertical collision
            if dy > 0:
                if collider_one_entity_dynamic == Application.Player:
                    collider_one_entity_dynamic.transform.position.y = rect_two.bottom - rect_one.height * 1.1
                else:
                    collider_one_entity_dynamic.transform.position.y = rect_two.bottom

            else:
                if collider_one_entity_dynamic == Application.Player:
                    collider_one_entity_dynamic.transform.position.y = rect_two.top - rect_one.height * 2.1
                else:
                    collider_one_entity_dynamic.transform.position.y = rect_two.top

    def __check_collision(self, box_collider_one, box_collider_two):

        collider_one_entity = box_collider_one.parent
        collider_two_entity = box_collider_two.parent

        collider_one = collider_one_entity.get_component(Collider)
        collider_two = collider_two_entity.get_component(Collider)

        if collider_one_entity == collider_two_entity:
            return

        if box_collider_one.collides_with(box_collider_two):
            self.__change_collision_layers_for_trees(collider_one_entity, collider_two_entity, RendererLayers.BelowPlayer)

            self.__handle_collision_physics(collider_one_entity, collider_two_entity)

            self.__handle_collision_responses(collider_one, collider_two, collider_one_entity, collider_two_entity)
        else:
            self.__handle_collision_exits(collider_one, collider_two)
            self.__change_collision_layers_for_trees(collider_one_entity, collider_two_entity, RendererLayers.AbovePlayer)


