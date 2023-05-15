from Engine.Graphics.Renderers.Renderer2D import Renderer2D

class RendererManager:
    def __init__(self, surface, scene_manager):
        self.__surface = surface
        self.__scene_manager = scene_manager

    def draw(self):
        renderers = self.__scene_manager.active_scene.get_all_components_by_type(Renderer2D)
        for renderer in renderers:
            renderer.draw(self.__surface)



