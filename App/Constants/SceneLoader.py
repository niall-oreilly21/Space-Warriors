import pygame
from pygame import Vector2

from App.Constants.Constants import Constants
from Engine.GameObjects.Components.Physics.ButtonColliderHover2D import ButtonColliderHover2D
from Engine.GameObjects.GameObject import GameObject
from Engine.Graphics.Materials.TextMaterial2D import TextMaterial2D
from Engine.Graphics.Materials.TextureMaterial2D import TextureMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Managers.Scene import Scene
from Engine.Other.Enums.GameObjectEnums import GameObjectCategory, GameObjectType
from Engine.Other.Transform2D import Transform2D


def initialise_menu_background(background_material):
    background = GameObject("MenuBackground", Transform2D(Vector2(0, 0), 0, Vector2(1, 1)))
    background.add_component(Renderer2D("MenuRenderer", background_material))

    return background


def initialise_menu(menu_scene, background_material, title_text, menu_button_text_top, menu_button_text_bottom,
                    top_button_name, bottom_button_name):
    background = initialise_menu_background(background_material)

    title = GameObject("MenuTitle", Transform2D(Vector2(0, 0), 0, Vector2(1, 1)), GameObjectType.Static,
                       GameObjectCategory.Menu)
    title_text_material = TextMaterial2D(Constants.Menu.TITLE_FONT_PATH, Constants.Menu.TITLE_FONT_SIZE, title_text,
                                         Vector2(Constants.VIEWPORT_WIDTH / 2, 200), (255, 255, 255))
    title.add_component(Renderer2D("TitleRenderer", title_text_material, 1))

    start_button = GameObject(top_button_name,
                              Transform2D(Vector2(Constants.VIEWPORT_WIDTH / 2 - 150, 330), 0, Vector2(1, 1)),
                              GameObjectType.Static, GameObjectCategory.Menu)
    start_button_texture_material = TextureMaterial2D(Constants.Menu.MENU_BUTTON_IMAGE, None,
                                                      Vector2(0, 0), None)

    start_button_text_material = TextMaterial2D(Constants.Menu.TEXT_FONT_PATH, Constants.Menu.TEXT_FONT_SIZE, menu_button_text_top,
                                                Vector2(150, 27), (0, 0, 0))
    start_button.add_component(Renderer2D("StartButtonRenderer", start_button_texture_material, 1))
    start_button.add_component(Renderer2D("StartButtonTextRenderer", start_button_text_material, 2))
    start_button.add_component(ButtonColliderHover2D("ButtonCollider", 0.05))

    end_button = start_button.clone()
    end_button.name = bottom_button_name
    end_button.transform.position.y = 440
    renderers = end_button.get_components(Renderer2D)

    for renderer in renderers:
        if isinstance(renderer.material, TextMaterial2D):
            renderer.material.text = menu_button_text_bottom

    menu_scene.add(background)
    menu_scene.add(title)
    menu_scene.add(start_button)
    menu_scene.add(end_button)


class SceneLoader:
    def __init__(self, camera_manager, camera_main_menu_game_object, scene_manager):
        self.__camera_manager = camera_manager
        self.__camera_main_menu_game_object = camera_main_menu_game_object
        self.__scene_manager = scene_manager

    def initialise_menu_scene(self, scene_name):
        self.__camera_manager.set_active_camera("MenuCamera")

        menu_scene = Scene(scene_name)
        menu_scene.add(self.__camera_main_menu_game_object)
        self.__scene_manager.add(scene_name, menu_scene)

        return menu_scene

    def initialise_level_menu(self, menu_scene):
        background = initialise_menu_background(Constants.Menu.MATERIAL_PAUSE_MENU)


        title = GameObject("MenuTitle", Transform2D(Vector2(0, 0), 0, Vector2(1, 1)), GameObjectType.Static,
                           GameObjectCategory.Menu)
        title_text_material = TextMaterial2D(Constants.Menu.TITLE_FONT_PATH, 30, "Land on...",
                                             Vector2(Constants.VIEWPORT_WIDTH / 2, 125), (255, 255, 255))
        title.add_component(Renderer2D("TitleRenderer", title_text_material, 1))

        earth = GameObject(Constants.Button.EARTH_BUTTON,
                           Transform2D(Vector2(Constants.VIEWPORT_WIDTH / 3 - 882 * 0.4, 260),
                                       0, Vector2(0.3, 0.3)), GameObjectType.Static, GameObjectCategory.Menu)
        earth_texture_material = TextureMaterial2D(Constants.Menu.EARTH_IMAGE, None,
                                                   Vector2(0, 0), None)
        earth.add_component(Renderer2D("EarthRenderer", earth_texture_material, 1))
        earth.add_component(ButtonColliderHover2D("ButtonCollider", 0.05))

        earth_text = GameObject("EarthText", Transform2D(Vector2(earth.transform.position.x + 130,
                                                                 earth.transform.position.y + 330), 0, Vector2(1, 1)),
                                GameObjectType.Static, GameObjectCategory.Menu)
        earth_text_material = TextMaterial2D(Constants.Menu.TEXT_FONT_PATH, 40, "Earth",
                                             Vector2(0, 0), (255, 255, 255))
        earth_text.add_component(Renderer2D("EarthTextRenderer", earth_text_material, 2))

        mars = earth.clone()
        mars.name = Constants.Button.MARS_BUTTON
        mars.transform.position.x = earth.transform.position.x + 883 * 0.3 + 150
        mars.get_component(Renderer2D).material.texture = Constants.Menu.MARS_IMAGE

        mars_text = earth_text.clone()
        mars_text.transform.position.x = mars.transform.position.x + 135
        mars_text.get_component(Renderer2D).material.text = "Mars"

        saturn = earth.clone()
        saturn.name = Constants.Button.SATURN_BUTTON
        saturn.transform.position.x = mars.transform.position.x + 883 * 0.3 + 100
        saturn_texture_material = TextureMaterial2D(Constants.Menu.SATURN_IMAGE, None,
                                                    Vector2(0, 0), None)
        saturn.get_component(Renderer2D).material = saturn_texture_material

        saturn_text = earth_text.clone()
        saturn_text.transform.position.x = saturn.transform.position.x + 240
        saturn_text.get_component(Renderer2D).material.text = "Saturn"

        menu_scene.add(background)
        menu_scene.add(title)
        menu_scene.add(earth)
        menu_scene.add(earth_text)
        menu_scene.add(mars)
        menu_scene.add(mars_text)
        menu_scene.add(saturn)
        menu_scene.add(saturn_text)
