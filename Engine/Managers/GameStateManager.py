import pygame

from App.Constants.Application import Application
from App.Constants.Constants import Constants
from Engine.GameObjects.Character import Character
from Engine.Graphics.Materials.TextMaterial2D import TextMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Managers.Manager import Manager
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.Enums.GameObjectEnums import GameObjectType, GameObjectCategory


class GameStateManager(Manager):
    def __init__(self, event_dispatcher, input_handler):
        super().__init__(event_dispatcher)
        self.__input_handler = input_handler
        self.__ui_helper_texts = []

    def _subscribe_to_events(self):
        self._event_dispatcher.add_listener(EventCategoryType.GameStateManager, self._handle_events)

    def _handle_events(self, event_data):
        if event_data.event_action_type == EventActionType.SetUITextHelper:
            ui_text = event_data.parameters[0]
            ui_text_game_object_name = event_data.parameters[1]
            self.__set_ui_text(ui_text, ui_text_game_object_name)

        elif event_data.event_action_type == EventActionType.TurnOnTeleporter:
            self.__set_up_teleporter()

        elif event_data.event_action_type == EventActionType.SetUpLevel:
            self.__set_up_level()

    def __set_ui_text(self, ui_text, ui_text_game_object_name):

        for ui_text_game_object in self.__ui_helper_texts:
            if ui_text_game_object.name == ui_text_game_object_name:

                ui_text_game_object.get_component(Renderer2D).material.text = ui_text

    def __set_up_level(self):
        if not Application.ActiveScene.contains(Application.Player):
            Application.ActiveScene.add(Application.Player)

        self.__dispatch_events_for_set_up_level()
        self.__position_characters_for_level()
        self.__set_up_teleporter_for_level()
        self.__get_ui_text_helpers()


    def __set_up_teleporter_for_level(self):
        teleporter = Application.ActiveScene.find_all_by_category(GameObjectType.Static, GameObjectCategory.Teleporter)[0]
        teleporter.get_component(SpriteAnimator2D).set_active_take(ActiveTake.TELEPORT_IDLE)

    def __position_characters_for_level(self):
        dynamic_game_object_list = Application.ActiveScene.find_all_by_type(GameObjectType.Dynamic)

        for game_object in dynamic_game_object_list:
            if isinstance(game_object, Character):
                game_object.transform.position = game_object.initial_position

    def __get_ui_text_helpers(self):
        self.__ui_helper_texts = Application.ActiveScene.find_all_by_category(GameObjectType.Static, GameObjectCategory.UIPrompts)

    def __dispatch_events_for_set_up_level(self):
        self._event_dispatcher.dispatch_event(EventData(EventCategoryType.CameraManager, EventActionType.SetCameraTarget, [Application.Player]))

        self._event_dispatcher.dispatch_event(EventData(EventCategoryType.RendererManager, EventActionType.TurnSpotLightOn))
        self._event_dispatcher.dispatch_event(EventData(EventCategoryType.CameraManager, EventActionType.GameCamera))
        self._event_dispatcher.dispatch_event(EventData(EventCategoryType.CollisionManager,EventActionType.SetUpColliders))

    def __set_up_teleporter(self):
        Application.ActiveScene.remove(Application.Player)

    def __check_pause_menu(self):
        if Application.ActiveScene.name == Constants.Scene.EARTH \
                or Application.ActiveScene.name == Constants.Scene.MARS \
                or Application.ActiveScene.name == Constants.Scene.SATURN:
            if self.__input_handler.is_tap(pygame.K_ESCAPE, 100):
                self._event_dispatcher.dispatch_event(EventData(EventCategoryType.SceneManager, EventActionType.PauseMenuScene))


    def update(self, game_time):
        self.__check_pause_menu()
        self.__input_handler.update()


