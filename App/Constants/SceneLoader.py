import pygame
from pygame import Vector2

from App.Constants.Application import Application
from App.Constants.GameConstants import GameConstants
from Engine.GameObjects.Components.Physics.ButtonColliderHover2D import ButtonColliderHover2D
from Engine.GameObjects.GameObject import GameObject
from Engine.Graphics.Materials.TextMaterial2D import TextMaterial2D
from Engine.Graphics.Materials.TextureMaterial2D import TextureMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Managers.Scene import Scene
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Enums.GameObjectEnums import GameObjectCategory, GameObjectType
from Engine.Other.Enums.RendererLayers import RendererLayers
from Engine.Other.Transform2D import Transform2D


def initialise_menu_background(background_material):
    background = GameObject("MenuBackground", Transform2D(Vector2(0, 0), 0, Vector2(1, 1)), GameObjectType.Static,
                            GameObjectCategory.UI)
    background.add_component(Renderer2D("MenuRenderer", background_material))

    return background


def initialise_back_button(menu_scene):
    back = GameObject(GameConstants.Button.BACK_BUTTON, Transform2D(Vector2(50, 50),
                                                                    0, Vector2(0.7, 0.7)), GameObjectType.Static,
                      GameObjectCategory.Menu)
    back.add_component(Renderer2D("ActivateRenderer", TextureMaterial2D(GameConstants.Menu.BACK_BUTTON_IMAGE, None,
                                                                        Vector2(0, 0), None), 1))
    back.add_component(ButtonColliderHover2D("ButtonColliderBack", 0.05))
    menu_scene.add(back)


def initialise_menu(menu_scene, background_material, title_text, button_texts):
    if menu_scene.name == GameConstants.Scene.SOUND_MENU or menu_scene.name == GameConstants.Scene.PAUSE_MENU:
        initialise_back_button(menu_scene)

    background = initialise_menu_background(background_material)

    title = GameObject("MenuTitle", Transform2D(Vector2(0, 0), 0, Vector2(1, 1)), GameObjectType.Static,
                       GameObjectCategory.MenuTitle)
    title_text_material = TextMaterial2D(GameConstants.Menu.TITLE_FONT_PATH, GameConstants.Menu.TITLE_FONT_SIZE,
                                         title_text,
                                         Vector2(GameConstants.VIEWPORT_WIDTH / 2, GameConstants.VIEWPORT_HEIGHT / 6),
                                         (255, 255, 255))
    title.add_component(Renderer2D("TitleRenderer", title_text_material, 1))

    button_positions = [
        Vector2(GameConstants.VIEWPORT_WIDTH / 2 - 150, GameConstants.VIEWPORT_HEIGHT / 6 * 2),
        Vector2(GameConstants.VIEWPORT_WIDTH / 2 - 150, GameConstants.VIEWPORT_HEIGHT / 6 * 3),
        Vector2(GameConstants.VIEWPORT_WIDTH / 2 - 150, GameConstants.VIEWPORT_HEIGHT / 6 * 4),
        Vector2(GameConstants.VIEWPORT_WIDTH / 2 - 150, GameConstants.VIEWPORT_HEIGHT / 6 * 5)
    ]
    for i in range(len(button_texts)):
        button_text = button_texts[i]
        button_position = button_positions[i]

        button = GameObject(button_text,
                            Transform2D(button_position, 0, Vector2(1, 1)),
                            GameObjectType.Static, GameObjectCategory.Menu)

        button_texture_material = TextureMaterial2D(GameConstants.Menu.MENU_BUTTON_IMAGE, None, Vector2(0, 0))
        button_text_material = TextMaterial2D(GameConstants.Menu.TEXT_FONT_PATH, GameConstants.Menu.TEXT_FONT_SIZE,
                                              button_text,
                                              Vector2(150, 27), (0, 0, 0))

        button.add_component(Renderer2D(f"{button_text}Renderer", button_texture_material, 1))
        button.add_component(Renderer2D(f"{button_text}TextRenderer", button_text_material, 2))
        button.add_component(ButtonColliderHover2D("ButtonCollider", 0.05))

        menu_scene.add(button)

    menu_scene.add(background)
    menu_scene.add(title)


def initialise_level_menu(menu_scene):
    initialise_back_button(menu_scene)
    background = initialise_menu_background(GameConstants.Menu.MATERIAL_PAUSE_MENU)

    title = GameObject("MenuTitle", Transform2D(Vector2(0, 0), 0, Vector2(1, 1)), GameObjectType.Static,
                       GameObjectCategory.MenuTitle)
    title_text_material = TextMaterial2D(GameConstants.Menu.TITLE_FONT_PATH, 30, "Land on...",
                                         Vector2(GameConstants.VIEWPORT_WIDTH / 2, 125), (255, 255, 255))
    title.add_component(Renderer2D("TitleRenderer", title_text_material, 1))

    earth = GameObject(GameConstants.Button.EARTH_BUTTON,
                       Transform2D(Vector2(GameConstants.VIEWPORT_WIDTH / 3 - 882 * 0.4, 260),
                                   0, Vector2(0.3, 0.3)), GameObjectType.Static, GameObjectCategory.Menu)
    earth_texture_material = TextureMaterial2D(GameConstants.Menu.EARTH_IMAGE, (120, 120, 120),
                                               Vector2(0, 0))
    earth.add_component(Renderer2D("EarthRenderer", earth_texture_material, 1))
    earth.add_component(ButtonColliderHover2D("ButtonCollider", 0.05))

    earth_text = GameObject("EarthText", Transform2D(Vector2(earth.transform.position.x + 130,
                                                             earth.transform.position.y + 330), 0, Vector2(1, 1)),
                            GameObjectType.Static, GameObjectCategory.Menu)
    earth_text_material = TextMaterial2D(GameConstants.Menu.TEXT_FONT_PATH, 40, "Earth",
                                         Vector2(0, 0), (255, 255, 255))
    earth_text.add_component(Renderer2D("EarthTextRenderer", earth_text_material, 2))

    mars = earth.clone()
    mars.name = GameConstants.Button.MARS_BUTTON
    mars.transform.position.x = earth.transform.position.x + 883 * 0.3 + 150
    mars_texture_material = TextureMaterial2D(GameConstants.Menu.MARS_IMAGE, (120, 120, 120),
                                              Vector2(0, 0))
    mars.get_component(Renderer2D).material = mars_texture_material

    mars_text = earth_text.clone()
    mars_text.transform.position.x = mars.transform.position.x + 135
    mars_text.get_component(Renderer2D).material.text = "Mars"

    saturn = earth.clone()
    saturn.name = GameConstants.Button.SATURN_BUTTON
    saturn.transform.position.x = mars.transform.position.x + 883 * 0.3 + 100
    saturn_texture_material = TextureMaterial2D(GameConstants.Menu.SATURN_IMAGE, (120, 120, 120),
                                                Vector2(0, 0))
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


def initialise_character_selection_menu(menu_scene):
    initialise_back_button(menu_scene)
    background = initialise_menu_background(GameConstants.Menu.MATERIAL_PAUSE_MENU)

    title = GameObject("MenuTitle", Transform2D(Vector2(0, 0), 0, Vector2(1, 1)), GameObjectType.Static,
                       GameObjectCategory.MenuTitle)
    title_text_material = TextMaterial2D(GameConstants.Menu.TITLE_FONT_PATH, 30, "Choose your warrior",
                                         Vector2(GameConstants.VIEWPORT_WIDTH / 2, 125), (255, 255, 255))
    title.add_component(Renderer2D("TitleRenderer", title_text_material, 1))

    girl_player = GameObject(GameConstants.Button.GIRL_PLAYER_BUTTON,
                             Transform2D(Vector2(GameConstants.VIEWPORT_WIDTH / 2 - 250, 295),
                                         0, Vector2(4, 4)),
                             GameObjectType.Static, GameObjectCategory.UI)
    material_player = GameConstants.Player.MATERIAL_GIRL
    girl_player.add_component(SpriteRenderer2D("player", material_player, RendererLayers.UI))
    girl_player.add_component(SpriteAnimator2D("player", GameConstants.Player.PLAYER_ANIMATOR_INFO, material_player,
                                               ActiveTake.PLAYER_MOVE_DOWN,
                                               GameConstants.CHARACTER_ANIMATOR_MOVE_SPEED))
    girl_player.add_component(ButtonColliderHover2D("ButtonColliderGirl", 0.6))

    boy_player = GameObject(GameConstants.Button.BOY_PLAYER_BUTTON,
                            Transform2D(Vector2(GameConstants.VIEWPORT_WIDTH / 2 + 150,
                                                295), 0, Vector2(4, 4)),
                            GameObjectType.Static, GameObjectCategory.UI)
    material_player = GameConstants.Player.MATERIAL_BOY
    boy_player.add_component(SpriteRenderer2D("player", material_player, RendererLayers.UI))
    boy_player.add_component(SpriteAnimator2D("player", GameConstants.Player.PLAYER_ANIMATOR_INFO, material_player,
                                              ActiveTake.PLAYER_MOVE_DOWN, GameConstants.CHARACTER_ANIMATOR_MOVE_SPEED))
    boy_player.add_component(ButtonColliderHover2D("ButtonColliderBoy", 0.6))

    girl_text = GameObject("GirlText", Transform2D(Vector2(girl_player.transform.position.x + 55,
                                                           girl_player.transform.position.y + 290), 0, Vector2(1, 1)),
                           GameObjectType.Static, GameObjectCategory.Menu)
    girl_text_material = TextMaterial2D(GameConstants.Menu.TEXT_FONT_PATH, 40, "Luna",
                                        Vector2(0, 0), (255, 255, 255))
    girl_text.add_component(Renderer2D("EarthTextRenderer", girl_text_material, 2))

    boy_text = GameObject("BoyText", Transform2D(Vector2(boy_player.transform.position.x + 55,
                                                         boy_player.transform.position.y + 290), 0, Vector2(1, 1)),
                          GameObjectType.Static, GameObjectCategory.Menu)
    boy_text_material = TextMaterial2D(GameConstants.Menu.TEXT_FONT_PATH, 40, "Apollo",
                                       Vector2(0, 0), (255, 255, 255))
    boy_text.add_component(Renderer2D("BoyTextRenderer", boy_text_material, 2))

    star = GameObject("Star", Transform2D(Vector2(120, 120), 0, Vector2(0.5, 0.5)), GameObjectType.Static,
                      GameObjectCategory.UI)
    material_star = GameConstants.Menu.MATERIAL_STARS
    star.add_component(SpriteRenderer2D("star", material_star, RendererLayers.WorldObjects))
    star.add_component(SpriteAnimator2D("star", GameConstants.Menu.STARS_ANIMATOR_INFO, material_star,
                                        ActiveTake.STAR, 5))

    star2 = star.clone()
    star2.transform.position = Vector2(1300, 160)
    star2.transform.scale = Vector2(0.4, 0.4)
    star2.get_component(SpriteAnimator2D).fps = 2

    star3 = star2.clone()
    star3.transform.position = Vector2(140, 500)
    star3.get_component(SpriteAnimator2D).fps = 2.5

    star4 = star2.clone()
    star4.transform.position = Vector2(350, 320)
    star4.transform.scale = Vector2(0.3, 0.3)
    star4.get_component(SpriteAnimator2D).fps = 4

    star5 = star.clone()
    star5.transform.position = Vector2(1320, 580)
    star5.transform.scale = Vector2(0.6, 0.6)
    star5.get_component(SpriteAnimator2D).fps = 6

    star6 = star4.clone()
    star6.transform.position = Vector2(1190, 400)
    star6.get_component(SpriteAnimator2D).fps = 3

    menu_scene.add(background)
    menu_scene.add(title)
    menu_scene.add(girl_player)
    menu_scene.add(boy_player)
    menu_scene.add(girl_text)
    menu_scene.add(boy_text)
    menu_scene.add(star)
    menu_scene.add(star2)
    menu_scene.add(star3)
    menu_scene.add(star4)
    menu_scene.add(star5)
    menu_scene.add(star6)


def initialise_controls_menu(menu_scene):
    initialise_back_button(menu_scene)
    background = initialise_menu_background(GameConstants.Menu.MATERIAL_PAUSE_MENU)

    title = GameObject("MenuTitle", Transform2D(Vector2(0, 0), 0, Vector2(1, 1)), GameObjectType.Static,
                       GameObjectCategory.MenuTitle)
    title_text_material = TextMaterial2D(GameConstants.Menu.TITLE_FONT_PATH, 30, "Controls",
                                         Vector2(GameConstants.VIEWPORT_WIDTH / 2, 125), (255, 255, 255))
    title.add_component(Renderer2D("TitleRenderer", title_text_material, 1))

    move = GameObject("MoveControls", Transform2D(Vector2(130, 200),
                                                  0, Vector2(0.6, 0.6)), GameObjectType.Static, GameObjectCategory.Menu)
    move.add_component(Renderer2D("MoveRenderer", TextureMaterial2D(GameConstants.Menu.MOVE_CONTROLS_IMAGE, None,
                                                                    Vector2(0, 0), None), 1))

    attack = GameObject("AttackControls", Transform2D(Vector2(GameConstants.VIEWPORT_WIDTH / 2 + 50, 200),
                                                      0, Vector2(0.6, 0.6)), GameObjectType.Static,
                        GameObjectCategory.Menu)
    attack.add_component(Renderer2D("AttackRenderer", TextureMaterial2D(GameConstants.Menu.ATTACK_CONTROLS_IMAGE, None,
                                                                        Vector2(0, 0), None), 1))

    activate = GameObject("ActivateControls", Transform2D(Vector2(GameConstants.VIEWPORT_WIDTH / 2 - 170, 600),
                                                          0, Vector2(0.6, 0.6)), GameObjectType.Static,
                          GameObjectCategory.Menu)
    activate.add_component(
        Renderer2D("ActivateRenderer", TextureMaterial2D(GameConstants.Menu.ACTIVATE_CONTROL_IMAGE, None,
                                                         Vector2(0, 0), None), 1))

    menu_scene.add(background)
    menu_scene.add(title)
    menu_scene.add(move)
    menu_scene.add(attack)
    menu_scene.add(activate)


class SceneLoader:
    def __init__(self, scene_manager):
        self.__scene_manager = scene_manager

    def initialise_menu_scene(self, scene_name):
        menu_scene = Scene(scene_name)
        self.__scene_manager.add(scene_name, menu_scene)

        return menu_scene
