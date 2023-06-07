import pygame
from pygame import Vector2, Rect

from App.Constants.Application import Application
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.Graphics.Materials.TextMaterial2D import TextMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Managers.CameraManager import CameraManager
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Managers.Manager import Manager
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.Enums.GameObjectEnums import GameObjectType, GameObjectCategory
from Engine.Other.Interfaces.IDrawable import IDrawable
from Engine.Other.Transform2D import Transform2D


class RendererManager(Manager, IDrawable):
    def __init__(self, surface, scene_manager, camera_manager, event_dispatcher):
        super().__init__(event_dispatcher)
        self.__surface = surface
        self.__scene_manager = scene_manager
        self.__camera_manager = camera_manager
        self.__is_debug_mode = False
        self.__is_spotlight_on = False


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


    def draw(self):
        renderers = self.__scene_manager.active_scene.get_all_components_by_type(Renderer2D)

        # Sort the renderers based on their layer depth
        renderers.sort(key=lambda renderer: renderer.layer)

        camera_component = self.__camera_manager.active_camera
        camera_position = camera_component.transform.position
        viewport = camera_component.viewport
        masked_surface = pygame.Surface(self.__surface.get_size(), pygame.SRCALPHA)


        for renderer in renderers:
            object_position = renderer.transform.position

            if renderer.parent.game_object_category == GameObjectCategory.UI or renderer.parent.game_object_category == GameObjectCategory.Menu or renderer.parent.game_object_category == GameObjectCategory.UIPrompts:
                renderer.draw(self.__surface,Transform2D(object_position, renderer.transform.rotation, renderer.transform.scale))

            else:
                object_draw_position = object_position - camera_position
                # Calculate the object's bounding rect in screen coordinates
                object_rect = renderer.get_bounding_rect(
                    Transform2D(object_draw_position, renderer.transform.rotation, renderer.transform.scale))

                # Check if the object's rect intersects with the camera's viewport

                # if self.__is_spotlight_on:
                #     if self.is_within_circle(object_draw_position, (750, 350), 200):
                #         renderer.draw(self.__surface, Transform2D(object_draw_position, renderer.transform.rotation,
                #                                                   renderer.transform.scale))
                #
                # else:
                if self.is_rect_visible(object_rect, viewport):
                    renderer.draw(self.__surface, Transform2D(object_draw_position, renderer.transform.rotation, renderer.transform.scale))

                    # # Apply a dark mask to the game object's surface
                    # dark_mask = pygame.Surface(renderer.material.texture.get_size(), pygame.SRCALPHA)
                    # dark_mask.fill((0, 0, 200, 255))
                    # # self.__surface.blit(renderer.material.texture,
                    # #                    (object_draw_position.x, object_draw_position.y),
                    # #                    special_flags=pygame.BLEND_RGBA_MULT)
                    # # Apply a dark mask to the game object's surface
                    # self.__surface.blit(dark_mask,
                    #                     (object_draw_position.x, object_draw_position.y),
                    #                     special_flags=pygame.BLEND_RGBA_MULT)

                    if self.__is_debug_mode:
                        self._event_dispatcher.dispatch_event(EventData(EventCategoryType.CollisionManager, EventActionType.DrawCollisionRange,[self.__surface, camera_position]))

                        if renderer.parent.get_component(BoxCollider2D):
                            renderer.parent.get_component(BoxCollider2D).draw(self.__surface, camera_position)


        # Blit the masked game objects onto the game surface
        #self.__surface.blit(masked_surface, (0, 0))

        # if self.__is_spotlight_on:
        #     self.draw_circle(camera_position)

    def is_rect_visible(self, rect, viewport):
        # Create a rectangle representing the camera's viewport
        camera_rect = Rect(0, 0, viewport.x + 60, viewport.y + 70)
        camera_rect.center = (viewport.x // 2, viewport.y // 2)

        # Check if the object's rect intersects with or is contained within the camera's viewport
        return rect.colliderect(camera_rect) or camera_rect.contains(rect)

    def is_within_circle(self, position, center, radius):
        distance_squared = (position[0] + 40 - center[0]) ** 2 + (position[1] - center[1]) ** 2
        return distance_squared < radius ** 2

    def draw_circle(self, camera_position):
        # Calculate the spotlight circle around the player
        spotlight_radius = 200  # Adjust the radius of the spotlight as desired

        draw_position = Application.Player.transform.position - camera_position
        spotlight_center = (750, 350)  # Center of the spotlight circle in the surface

        # Create a temporary surface for the spotlight (size of the spotlight circle)
        spotlight_surface = pygame.Surface((spotlight_radius * 2, spotlight_radius * 2), pygame.SRCALPHA)

        # Draw the circular shape on the spotlight surface with a bright color
        pygame.draw.circle(spotlight_surface, (100, 200, 100, 255), (spotlight_radius, spotlight_radius),
                           spotlight_radius)

        # Create a circular mask for the spotlight
        mask = pygame.Surface((spotlight_radius * 2, spotlight_radius * 2), pygame.SRCALPHA)
        #pygame.draw.circle(mask, (0, 0, 0, 255), (spotlight_radius, spotlight_radius), spotlight_radius)

        # Calculate the position to blit the spotlight surface on the game surface
        blit_position = draw_position - Vector2(spotlight_radius, spotlight_radius)

        # Blit the spotlight surface onto the game surface with a brighter blending mode
        self.__surface.blit(spotlight_surface, (blit_position.x, blit_position.y),
                            special_flags=pygame.BLEND_RGBA_ADD)

    # Rest of your code...

    # Rest of your code...









