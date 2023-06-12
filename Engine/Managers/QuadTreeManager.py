from abc import ABC

from App.Constants.Application import Application
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.QuadTree.CollisionRange import CollisionRange
from Engine.QuadTree.QuadTree import QuadTree
from Engine.Managers.Manager import Manager
from Engine.Other.Enums.GameObjectEnums import GameObjectType


class QuadTreeManager(Manager,  ABC):
    def __init__(self, map_dimensions, collision_range_target, collision_range_width, collision_range_height, quad_tree_capacity, event_dispatcher, component_type = None):
        super().__init__(event_dispatcher)
        self._components = None
        self.__map_dimensions = map_dimensions
        self.__quad_tree_capacity = quad_tree_capacity
        self._collision_range = CollisionRange(0, 0, collision_range_width, collision_range_height)
        self._dynamic_objects_components = []
        self._collision_range_target = collision_range_target
        self.__component_type = component_type
        self._collision_range_target_box_collider = None
        self._quad_tree = QuadTree(self.__map_dimensions, self.__quad_tree_capacity)

    @property
    def collision_range(self):
        return self._collision_range

    def start(self):
        self._set_up_component_list_and_quad_tree()
        self.__insert_into_quad_tree()
        self.__set_up_dynamic_game_objects_list()

    def _set_up_component_list_and_quad_tree(self):
        self._components = Application.ActiveScene.get_all_components_by_type(self.__component_type)
        self._quad_tree.clear()
        self._dynamic_objects_components.clear()
        self._collision_range_target_box_collider = self._collision_range_target.get_component(BoxCollider2D)

    def __insert_into_quad_tree(self):
        for component in self._components:
            self._quad_tree.insert(component)


    def __set_up_dynamic_game_objects_list(self):
        dynamic_game_objects = Application.ActiveScene.find_all_by_type(GameObjectType.Dynamic)

        for game_object in dynamic_game_objects:
            if game_object.get_component(self.__component_type):
                self._dynamic_objects_components.append(game_object.get_component(self.__component_type))

    def _clear_scene(self):
        if self._quad_tree:
            self._quad_tree.clear()

    def update(self, game_time):
        self._update_collision_range()

    def _get_potential_components(self):
        objects_in_range = self._quad_tree.query(self._collision_range.bounds)

        self._update_dynamic_game_objects_in_quad_tree(objects_in_range)
        return objects_in_range


    def _update_dynamic_game_objects_in_quad_tree(self, objects_in_range):
        for game_object_component in self._dynamic_objects_components:
            if game_object_component in objects_in_range:
                self._quad_tree.remove(game_object_component)
                self._quad_tree.insert(game_object_component)

    def _update_collision_range(self):
        self._collision_range.x = self._collision_range_target_box_collider.bounds.centerx - self._collision_range.width / 2
        self._collision_range.y = self._collision_range_target_box_collider.bounds.centery - self._collision_range.height / 2


    def _add_component(self, component):
        if component.parent.game_object_type is GameObjectType.Dynamic:
            self._dynamic_objects_components.append(component)

        self._quad_tree.insert(component)

    def _remove_component(self, component):
        if component.parent.game_object_type is GameObjectType.Dynamic:
            self._dynamic_objects_components.remove(component)

        self._quad_tree.remove(component)

