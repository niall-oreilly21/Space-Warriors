import pygame
from pygame import Vector2, Rect

from App.Constants.Application import Application
from App.Constants.GameConstants import GameConstants
from App.Constants.GameObjectConstants import GameObjectConstants
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Managers.QuadTreeManager import QuadTreeManager
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.Enums.GameObjectEnums import GameObjectType, GameObjectCategory
from Engine.Other.Interfaces.IDrawable import IDrawable
from Engine.Other.Transform2D import Transform2D


class RendererManager(QuadTreeManager, IDrawable):
    def __init__(self, surface, event_dispatcher, map_dimensions, collision_range_target, collision_range_width, collision_range_height, quad_tree_capacity, component_type = Renderer2D):
        super().__init__(map_dimensions, collision_range_target, collision_range_width, collision_range_height, quad_tree_capacity, event_dispatcher, component_type)
        self.__is_menu = True
        self.__surface = surface
        self.__is_debug_mode = False
        self.__is_spotlight_on = False
        self.__game_objects_rects = None
        self.__text_renderers = []
        self.__camera_position = None

    @property
    def is_debug_mode(self):
        return self.__is_debug_mode

    @is_debug_mode.setter
    def is_debug_mode(self, is_debug_mode):
        self.__is_debug_mode = is_debug_mode

    def _subscribe_to_events(self):
        self._event_dispatcher.add_listener(EventCategoryType.RendererManager, self._handle_events)

    def _handle_events(self, event_data):
        if event_data.event_action_type == EventActionType.DebugModeOn:
            self.__is_debug_mode = True

        elif event_data.event_action_type == EventActionType.DebugModeOff:
            self.__is_debug_mode = False

        elif event_data.event_action_type == EventActionType.TurnSpotLightOn:
            self.__is_spotlight_on = True

        elif event_data.event_action_type == EventActionType.TurnSpotLightOff:
            self.__is_spotlight_on = False

        elif event_data.event_action_type == EventActionType.IsMenu:
            self.__is_menu = True

        elif event_data.event_action_type == EventActionType.IsGame:
            self.__is_menu = False

        elif event_data.event_action_type == EventActionType.SetUpRenderers:
            self.start()

        elif event_data.event_action_type == EventActionType.AddRendererToQuadTree:
            renderer = event_data.parameters[0]
            self._add_component(renderer)

        elif event_data.event_action_type == EventActionType.RemoveRendererFromQuadTree:
            renderer = event_data.parameters[0]
            self._remove_component(renderer)

        elif event_data.event_action_type == EventActionType.SetRendererQuadTreeTarget:
            target = event_data.parameters[0]
            self._collision_range_target = target

            if self._collision_range_target.name == GameObjectConstants.Teleporter.TELEPORTER_NAME:
                self._collision_range.width += GameConstants.VIEWPORT_WIDTH + 60
            else:
                self._collision_range.width = GameConstants.VIEWPORT_WIDTH + 10

            self._collision_range_target_box_collider = target.get_component(BoxCollider2D)

    def start(self):
        self._set_up_component_list_and_quad_tree()

        for renderer in self._components:
            if renderer.parent.game_object_category == GameObjectCategory.UI or renderer.parent.game_object_category == GameObjectCategory.UIPrompts:
                self.__text_renderers.append(renderer)

            else:
                self.__calculate_draw_position(renderer)
                self._quad_tree.insert(renderer)

                if renderer.parent.game_object_type is GameObjectType.Dynamic:
                    self._dynamic_objects_components.append(renderer)

        self.__text_renderers.sort(key=lambda renderer: renderer.layer)


    def __calculate_draw_position(self, renderer):
        material_source_rect = renderer.material.source_rect

        if isinstance(renderer, SpriteRenderer2D):
            if renderer.sprite:
                material_source_rect = renderer.sprite.source_rect

            elif renderer.parent.get_component(SpriteAnimator2D):
                material_source_rect = renderer.parent.get_component(SpriteAnimator2D).get_current_sprite().source_rect

        renderer.bounds = material_source_rect

    def _update_dynamic_game_objects_in_quad_tree(self, objects_in_range):
        for renderer in self._dynamic_objects_components:
            if renderer in objects_in_range:
                self._quad_tree.remove(renderer)
                self.__calculate_draw_position(renderer)
                self._quad_tree.insert(renderer)

    def draw(self):
        self.__camera_position = Application.ActiveCamera.transform.position

        if self.__is_menu:
            self.__draw_menu()

        else:
            self.__draw_game()


    def __draw_game(self):
        self._update_collision_range()
        potential_renderers = self._get_potential_components()

        # Sort the renderers based on their layer depth
        potential_renderers.sort(key=lambda renderer: renderer.layer)

        for renderer in potential_renderers:
            renderer.draw(self.__surface, Transform2D(renderer.transform.position - self.__camera_position, renderer.transform.rotation, renderer.transform.scale))

            if self.__is_debug_mode:
                self._event_dispatcher.dispatch_event(
                    EventData(EventCategoryType.CollisionManager, EventActionType.DrawCollisionRange, [self.__surface, Application.ActiveCamera.transform.position]))

                if renderer.parent.get_component(BoxCollider2D):
                    renderer.parent.get_component(BoxCollider2D).draw(self.__surface, Application.ActiveCamera.transform.position)

        for renderer in self.__text_renderers:
            renderer.draw(self.__surface, Transform2D(renderer.transform.position, renderer.transform.rotation, renderer.transform.scale))


        if self.__is_spotlight_on:
            self.draw_spotlight()

    def __draw_menu(self):
        renderers = Application.ActiveScene.get_all_components_by_type(Renderer2D)

        # Sort the renderers based on their layer depth
        renderers.sort(key=lambda renderer: renderer.layer)

        for renderer in renderers:
            object_position = renderer.transform.position
            renderer.draw(self.__surface, Transform2D(object_position, renderer.transform.rotation, renderer.transform.scale))


    def draw_spotlight(self):
        # Calculate the spotlight circle around the player
        spotlight_radius = 200

        # Create a mask for the spotlight
        spotlight_surface = pygame.Surface((self.__surface.get_width(), self.__surface.get_height()), pygame.SRCALPHA)
        spotlight_surface.fill((0, 0, 0, 175))

        screen_center = Vector2(self.__surface.get_width() / 2 + 10, self.__surface.get_height() / 2 + 40)

        blit_position = screen_center - Vector2(spotlight_radius, spotlight_radius)

        light = pygame.image.load("Assets/UI/circle.png")

        spotlight_surface.blit(light, (blit_position.x, blit_position.y), special_flags=pygame.BLEND_RGBA_SUB)

        self.__surface.blit(spotlight_surface, (0, 0))

