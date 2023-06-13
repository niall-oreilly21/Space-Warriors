from App.Components.Colliders.AttackBoxCollider2D import AttackBoxCollider2D
from App.Constants.Application import Application
from Engine.GameObjects.Character import Character
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Collider import Collider
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Managers.QuadTreeManager import QuadTreeManager
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.Enums.GameObjectEnums import GameObjectCategory
from Engine.Other.Enums.RendererLayers import RendererLayers


class CollisionManager(QuadTreeManager):
    def __init__(self, map_dimensions, collision_range_target, collision_range_width, collision_range_height, quad_tree_capacity, event_dispatcher, component_type = BoxCollider2D):
        super().__init__( map_dimensions, collision_range_target, collision_range_width, collision_range_height, quad_tree_capacity, event_dispatcher, component_type)
        self.__collision_range_target_box_collider = None
        self.__update = False

    def _subscribe_to_events(self):
        self._event_dispatcher.add_listener(EventCategoryType.CollisionManager, self._handle_events)

    def _handle_events(self, event_data):
        if event_data.event_action_type == EventActionType.SetUpColliders:
            self.start()

        elif event_data.event_action_type == EventActionType.RemoveColliderFromQuadTree:
            box_collider = event_data.parameters[0]
            self._remove_component(box_collider)

        elif event_data.event_action_type == EventActionType.AddColliderToQuadTree:
            box_collider = event_data.parameters[0]
            self._add_component(box_collider)

        elif event_data.event_action_type == EventActionType.DrawCollisionRange:
            screen = event_data.parameters[0]
            camera_position = event_data.parameters[1]
            if self.__update:
                self._collision_range.draw(screen, camera_position)

        elif event_data.event_action_type == EventActionType.TurnOffCollisionDetection:
            self.__update = False

        elif event_data.event_action_type == EventActionType.TurnOnCollisionDetection:
            self.__update = True


    def start(self):
        super().start()

    def update(self, game_time):
        if self.__update:
            super().update(game_time)

            potential_colliders = self._get_potential_components()

            for i in range(len(potential_colliders)):
                box_collider_one = potential_colliders[i]

                if box_collider_one.parent.get_component(Collider):
                    box_collider_one.parent.get_component(Collider).is_colliding = False

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

    def __ignore_physics_collisions(self, collider_one_entity, collider_two_entity):
        return collider_one_entity.game_object_category is GameObjectCategory.Teleporter or collider_two_entity.game_object_category is GameObjectCategory.Teleporter \
        or collider_one_entity.game_object_category is GameObjectCategory.PowerUp or collider_two_entity.game_object_category is GameObjectCategory.PowerUp \
        or isinstance(collider_one_entity.get_component(BoxCollider2D), AttackBoxCollider2D) or isinstance(collider_two_entity.get_component(BoxCollider2D), AttackBoxCollider2D)


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
            if collider_one:
                collider_one.is_colliding = True

            if collider_two:
                collider_two.is_colliding = True
            self.__handle_collision_responses(collider_one, collider_two, collider_one_entity, collider_two_entity)
            self.__change_collision_layers_for_trees(collider_one_entity, collider_two_entity, RendererLayers.BelowPlayer)

            self.__handle_collision_physics(collider_one_entity, collider_two_entity)
        else:
            if collider_one and collider_two:
                if not collider_one.is_colliding and not collider_two.is_colliding:
                    self.__handle_collision_exits(collider_one, collider_two)

            self.__change_collision_layers_for_trees(collider_one_entity, collider_two_entity, RendererLayers.AbovePlayer)


