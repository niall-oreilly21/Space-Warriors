from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Managers.CameraManager import CameraManager
from Engine.Other.Transform2D import Transform2D


class RendererManager:
    def __init__(self, surface, scene_manager, camera_manager : CameraManager):
        self.__surface = surface
        self.__scene_manager = scene_manager
        self.__camera_manager = camera_manager

    def draw(self, game_time):
        renderers = self.__scene_manager.active_scene.get_all_components_by_type(Renderer2D)
        for renderer in renderers:
            object_draw_position = renderer.transform.position - self.__camera_manager.active_camera.transform.position
            renderer.draw(self.__surface, Transform2D(object_draw_position, renderer.transform.rotation, renderer.transform.scale))



