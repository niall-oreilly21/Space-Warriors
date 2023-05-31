from pygame import Vector2, Rect

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

    def draw(self):
        renderers = self.__scene_manager.active_scene.get_all_components_by_type(Renderer2D)

        # Sort the renderers based on their layer depth
        renderers.sort(key=lambda renderer: renderer.layer)

        camera_component = self.__camera_manager.active_camera
        camera_position = camera_component.transform.position
        viewport = camera_component.viewport

        for renderer in renderers:
            object_position = renderer.transform.position

            if renderer.parent.game_object_category == GameObjectCategory.UI or renderer.parent.game_object_category == GameObjectCategory.Menu:
                renderer.draw(self.__surface,Transform2D(object_position, renderer.transform.rotation, renderer.transform.scale))

            else:
                object_draw_position = object_position - camera_position
                # Calculate the object's bounding rect in screen coordinates
                object_rect = renderer.get_bounding_rect(
                    Transform2D(object_draw_position, renderer.transform.rotation, renderer.transform.scale))

                # Check if the object's rect intersects with the camera's viewport
                if self.is_rect_visible(object_rect, viewport):
                    renderer.draw(self.__surface,
                                  Transform2D(object_draw_position, renderer.transform.rotation,
                                              renderer.transform.scale))

                    if self.__is_debug_mode:
                        if renderer.parent.get_component(BoxCollider2D):
                            renderer.parent.get_component(BoxCollider2D).draw(self.__surface, camera_component.transform.position)

    def is_rect_visible(self, rect, viewport):
        # Create a rectangle representing the camera's viewport
        camera_rect = Rect(0, 0, viewport.x + 100, viewport.y + 100)
        camera_rect.center = (viewport.x // 2, viewport.y // 2)

        # Check if the object's rect intersects with or is contained within the camera's viewport
        return rect.colliderect(camera_rect) or camera_rect.contains(rect)




