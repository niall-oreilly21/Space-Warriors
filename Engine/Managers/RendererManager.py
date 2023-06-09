import time

import pygame
from pygame import Vector2, Rect

from App.Constants.Application import Application
from App.Constants.Constants import Constants
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.CollisionRange import CollisionRange
from Engine.GameObjects.Components.Physics.QuadTree import QuadTree
from Engine.GameObjects.Tiles.Tile import Tile
from Engine.Graphics.Materials.TextMaterial2D import TextMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Managers.CameraManager import CameraManager
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Managers.Manager import Manager
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.Enums.GameObjectEnums import GameObjectType, GameObjectCategory
from Engine.Other.Interfaces.IDrawable import IDrawable
from Engine.Other.Transform2D import Transform2D


class RendererManager(Manager, IDrawable):
    def __init__(self, surface, event_dispatcher):
        super().__init__(event_dispatcher)
        self.is_menu = True
        self.__surface = surface
        self.__is_debug_mode = False
        self.__is_spotlight_on = False
        self.__collision_range = None
        self.__quad_tree = None
        self.__game_objects_rects = None
        self.__dynamic_objects_renderers = []
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

    def start(self):
        self.__quad_tree = QuadTree(pygame.Rect(0, 0, 110 * 72, 120 * 72), 8)
        self.__collision_range = CollisionRange(0, 0, Application.ActiveCamera.viewport.x + 60, Application.ActiveCamera.viewport.y + 90)
        renderers = Application.ActiveScene.get_all_components_by_type(Renderer2D)

        # self.__tiles = {Constants.Tile.GRASS:}

        for renderer in renderers:
            if renderer.parent.game_object_category == GameObjectCategory.UI or renderer.parent.game_object_category == GameObjectCategory.Menu or renderer.parent.game_object_category == GameObjectCategory.UIPrompts:
                self.__text_renderers.append(renderer)

            else:
                self.__calculate_draw_position(renderer)
                self.__quad_tree.insert(renderer)

                if renderer.parent.game_object_type is GameObjectType.Dynamic:
                    self.__dynamic_objects_renderers.append(renderer)


    def __calculate_draw_position(self, renderer):
        material_source_rect = renderer.material.source_rect

        if isinstance(renderer, SpriteRenderer2D):
            if renderer.parent.get_component(SpriteAnimator2D):
                material_source_rect = renderer.parent.get_component(SpriteAnimator2D).get_current_sprite().source_rect
            elif renderer.sprite:
                material_source_rect = renderer.sprite.source_rect

        renderer.bounds = material_source_rect


    def __update_collision_range(self):
        self.__collision_range.x = self.__player_bounds.centerx - self.__collision_range.width / 2
        self.__collision_range.y = self.__player_bounds.centery - self.__collision_range.height / 2

    def __update_dynamic_game_objects_renderers_in_quad_tree(self):
        for renderer in self.__dynamic_objects_renderers:
            self.__quad_tree.remove(renderer)
            self.__calculate_draw_position(renderer)
            self.__quad_tree.insert(renderer)

    def draw(self):
        self.__camera_position = Application.ActiveCamera.transform.position
        self.__player_bounds = Application.Player.get_component(BoxCollider2D).bounds

        if self.is_menu:
            self.__draw_menu()

        else:
            self.__update_collision_range()
            self.__update_dynamic_game_objects_renderers_in_quad_tree()

            potential_renderers = self.__quad_tree.query(self.__collision_range.bounds)

            # Sort the renderers based on their layer depth
            potential_renderers.sort(key=lambda renderer: renderer.layer)

            for renderer in potential_renderers:
                renderer.draw(self.__surface,
                              Transform2D(renderer.transform.position - self.__camera_position,
                                          renderer.transform.rotation, renderer.transform.scale))

                # if self.__is_debug_mode:
                #     self._event_dispatcher.dispatch_event(
                #         EventData(EventCategoryType.CollisionManager, EventActionType.DrawCollisionRange,
                #                   [self.__surface, Application.ActiveCamera.transform.position]))
                #
                #     if renderer.parent.get_component(BoxCollider2D):
                #         renderer.parent.get_component(BoxCollider2D).draw(self.__surface, Application.ActiveCamera.transform.position)

    def __draw_menu(self):
        renderers = Application.ActiveScene.get_all_components_by_type(Renderer2D)

        # Sort the renderers based on their layer depth
        renderers.sort(key=lambda renderer: renderer.layer)

        camera_component = Application.ActiveCamera
        camera_position = camera_component.transform.position
        viewport = camera_component.viewport

        for renderer in renderers:
            object_position = renderer.transform.position

            if renderer.parent.game_object_category == GameObjectCategory.UI or renderer.parent.game_object_category == GameObjectCategory.Menu or renderer.parent.game_object_category == GameObjectCategory.UIPrompts:
                renderer.draw(self.__surface,
                              Transform2D(object_position, renderer.transform.rotation, renderer.transform.scale))

            else:
                object_draw_position = object_position - camera_position

                object_rect = renderer.get_bounding_rect(
                    Transform2D(object_draw_position, renderer.transform.rotation, renderer.transform.scale))

                # else:
                if self.is_rect_visible(object_rect, viewport):
                    renderer.draw(self.__surface, Transform2D(object_draw_position, renderer.transform.rotation,
                                                              renderer.transform.scale))

                    if self.__is_debug_mode:
                        self._event_dispatcher.dispatch_event(
                            EventData(EventCategoryType.CollisionManager, EventActionType.DrawCollisionRange,
                                      [self.__surface, camera_position]))

                        if renderer.parent.get_component(BoxCollider2D):
                            renderer.parent.get_component(BoxCollider2D).draw(self.__surface, camera_position)

        if self.__is_spotlight_on:
            self.draw_spotlight()


    def is_rect_visible(self, rect, viewport):
        # Create a rectangle representing the camera's viewport
        camera_rect = Rect(0, 0, viewport.x + 60, viewport.y + 70)
        camera_rect.center = (viewport.x // 2, viewport.y // 2)

        # Check if the object's rect intersects with or is contained within the camera's viewport
        return rect.colliderect(camera_rect) or camera_rect.contains(rect)

    def draw_spotlight(self):
        # Calculate the spotlight circle around the player
        spotlight_radius = 200

        # Create a mask for the spotlight
        spotlight_surface = pygame.Surface((self.__surface.get_width(), self.__surface.get_height()), pygame.SRCALPHA)
        spotlight_surface.fill((0, 0, 0, 225))

        screen_center = Vector2(self.__surface.get_width() / 2 + 10, self.__surface.get_height() / 2 + 40)

        blit_position = screen_center - Vector2(spotlight_radius, spotlight_radius)

        light = pygame.image.load("Assets/UI/circle.png")

        spotlight_surface.blit(light, (blit_position.x, blit_position.y), special_flags=pygame.BLEND_RGBA_SUB)

        self.__surface.blit(spotlight_surface, (0, 0))

