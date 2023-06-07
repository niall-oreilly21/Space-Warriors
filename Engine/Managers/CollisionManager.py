import pygame
from App.Constants.Application import Application
from Engine.GameObjects.Character import Character
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Collider import Collider
from Engine.GameObjects.Components.Physics.CollisionArea import CollisionArea
from Engine.GameObjects.Components.Physics.QuadTree import QuadTree
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Managers.Manager import Manager
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.Enums.GameObjectEnums import GameObjectType
from Engine.Other.Enums.RendererLayers import RendererLayers


class CollisionManager(Manager):
    def __init__(self, collision_range, scene_manager, camera_manager, event_dispatcher):
        super().__init__(event_dispatcher)
        self.__colliders = None
        self.__collision_range = collision_range
        self.__scene_manager = scene_manager
        self.__camera_manager = camera_manager
        self.collision_area = CollisionArea(0, 0, 500, 500)

        self.quad_tree = QuadTree(self.collision_area.boundary, 4)
        self.dynamic_objects_colliders = []
        self.__player_box_collider = None

    def _subscribe_to_events(self):
        self._event_dispatcher.add_listener(EventCategoryType.CollisionManager, self._handle_events)

    def _handle_events(self, event_data):
        if event_data.event_action_type == EventActionType.SetUpColliders:
            self.start()

        elif event_data.event_action_type == EventActionType.RemoveCollliderFromQuadTree:
            collider = event_data.parameters[0]
            self.quad_tree.remove(collider)

    def start(self):
        self.__colliders = self.__scene_manager.active_scene.get_all_components_by_type(BoxCollider2D)
        dynamic_objects = self.__scene_manager.active_scene.find_all_by_type(GameObjectType.Dynamic)

        for object in dynamic_objects:
            self.dynamic_objects_colliders.append(object.get_component(BoxCollider2D))

        self.quad_tree = QuadTree(pygame.Rect(0, 0, 110 * 72, 120 * 72), 4)

        for collider in self.__colliders:
            self.quad_tree.insert(collider)

        self.quad_tree.print_quadtree()

        self.__player_box_collider = Application.Player.get_component(BoxCollider2D)

    def update_collision_area(self):
        camera = self.__camera_manager.active_camera
        viewport = camera.viewport
        target_position = Application.Player.transform.position

        player_bounds = self.__player_box_collider.bounds

        # Calculate the top-left coordinates to center the collision area
        self.collision_area.x = player_bounds.centerx - self.collision_area.width / 2
        self.collision_area.y = player_bounds.centery - self.collision_area.height / 2

    def collision_area(self):
        return self.collision_area

    def update(self, game_time):
        self.update_collision_area()

        for collider in self.dynamic_objects_colliders:
            self.quad_tree.remove(collider)

        for collider in self.dynamic_objects_colliders:
            self.quad_tree.insert(collider)

        potential_colliders = list(self.quad_tree.query(self.collision_area.boundary))

        for i in range(len(potential_colliders)):
            box_collider_one = potential_colliders[i]
            for j in range(i + 1, len(potential_colliders)):
                box_collider_two = potential_colliders[j]
                self.__check_collision(box_collider_one, box_collider_two)

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

    def __handle_collision_physics(self, collider_one_entity, collider_two_entity):
        collider_one_rigidbody = collider_one_entity.get_component(Rigidbody2D)
        collider_two_rigidbody = collider_two_entity.get_component(Rigidbody2D)

        is_collider1_static = collider_one_entity.game_object_type.Static
        is_collider2_static = collider_two_entity.game_object_type.Static

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
            self.__change_collision_layers_for_trees(collider_one_entity, collider_two_entity, RendererLayers.WorldObjects)

            self.__handle_collision_physics(collider_one_entity, collider_two_entity)

            self.__handle_collision_responses(collider_one, collider_two, collider_one_entity, collider_two_entity)
        else:
            self.__handle_collision_exits(collider_one, collider_two)
            self.__change_collision_layers_for_trees(collider_one_entity, collider_two_entity, RendererLayers.Tree)
