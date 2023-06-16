import pygame
from pygame import Vector2

from App.Constants.Application import Application
from App.Constants.GameConstants import GameConstants
from App.Constants.EntityConstants import EntityConstants
from Engine.GameObjects.Character import Character
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Managers.Manager import Manager
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.Enums.GameObjectEnums import GameObjectType, GameObjectCategory


class GameStateManager(Manager):
    def __init__(self, event_dispatcher, input_handler, map_loader):
        super().__init__(event_dispatcher)
        self.__input_handler = input_handler
        self.__ui_helper_texts = []
        self.__map_loader = map_loader
        self.__enemies_in_scene_count = GameConstants.DEFAULT_ENEMIES
        self.__level_complete = False

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

        elif event_data.event_action_type == EventActionType.SetUpHouseLevel:
            self.__set_up_base_level()

        elif event_data.event_action_type == EventActionType.LoadLevel:
            self.__load_level()

        elif event_data.event_action_type == EventActionType.RemoveEnemyFromScene:
            self.__enemies_in_scene_count -= 1

        elif event_data.event_action_type == EventActionType.ReloadEarthScene:
            self.__reload_earth_scene()

    def __set_ui_text(self, ui_text, ui_text_game_object_name):

        for ui_text_game_object in self.__ui_helper_texts:
            if ui_text_game_object.name == ui_text_game_object_name:

                ui_text_game_object.get_component(Renderer2D).material.text = ui_text

                if ui_text == "":
                    ui_text_game_object.get_component(Renderer2D).is_drawing = False
                else:
                    ui_text_game_object.get_component(Renderer2D).is_drawing = True

    def __set_up_level(self):
        Application.GameStarted = False
        if Application.ActiveScene.name is GameConstants.Scene.EARTH:
            self.__enemies_in_scene_count = self.__map_loader.load_house_dynamic_objects()
            self.__enemies_in_scene_count += self.__map_loader.load_planet_dynamic_objects(Application.ActiveScene)
        else:
            self.__enemies_in_scene_count = self.__map_loader.load_planet_dynamic_objects(Application.ActiveScene)

        Application.GameStarted = True
        self.__level_complete = False
        self.__set_up_base_level()

    def __reload_earth_scene(self):
        Application.Player.transform.position = Vector2(2945, 2860)
        self.__set_up_events()

    def __set_up_base_level(self):
        self.__set_up_events()
        self.__position_characters_for_level()
        self.__map_loader.load_pet(Application.ActiveScene)

    def __set_up_events(self):
        self.__dispatch_events_for_set_up_level()
        self.__get_ui_text_helpers()


    def __set_up_teleporter_for_level(self):
        teleporters = Application.ActiveScene.find_all_by_category(GameObjectType.Static, GameObjectCategory.Teleporter)

        if not teleporters:
            return

        teleporters[0].get_component(SpriteAnimator2D).set_active_take(ActiveTake.TELEPORT_IDLE)

    def __position_characters_for_level(self):
        dynamic_game_object_list = Application.ActiveScene.find_all_by_type(GameObjectType.Dynamic)

        for game_object in dynamic_game_object_list:
            if isinstance(game_object, Character):
                if game_object is Application.Player:
                    self.__reset_player_position()

                game_object.reset_position()

                if Application.ActiveScene.name != GameConstants.Scene.HOUSE:
                    game_object.reset_health()

    def __reset_player_position(self):
        if Application.ActiveScene.name is GameConstants.Scene.EARTH:
            Application.Player.initial_position = EntityConstants.Player.PLAYER_INITIAL_POSITION_EARTH

        if Application.ActiveScene.name is GameConstants.Scene.MARS:
            Application.Player.initial_position = EntityConstants.Player.PLAYER_INITIAL_POSITION_MARS

        if Application.ActiveScene.name is GameConstants.Scene.SATURN:
            Application.Player.initial_position = EntityConstants.Player.PLAYER_INITIAL_POSITION_SATURN

        if Application.ActiveScene.name is GameConstants.Scene.HOUSE:
            Application.Player.initial_position = EntityConstants.Player.PLAYER_INITIAL_POSITION_HOUSE

    def __get_ui_text_helpers(self):
        self.__ui_helper_texts = Application.ActiveScene.find_all_by_category(GameObjectType.Static, GameObjectCategory.UIPrompts)

    def __dispatch_events_for_set_up_level(self):
        self.__dispatch_events_for_load_up_level()
        self._event_dispatcher.dispatch_event(EventData(EventCategoryType.CollisionManager,EventActionType.SetUpColliders))
        self._event_dispatcher.dispatch_event(EventData(EventCategoryType.RendererManager, EventActionType.SetUpRenderers))
        self._event_dispatcher.dispatch_event(EventData(EventCategoryType.RendererManager, EventActionType.SetRendererQuadTreeTarget, [Application.Player]))
        self._event_dispatcher.dispatch_event(EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,["",GameConstants.UITextPrompts.UI_TEXT_BOTTOM]))
        self.__check_turn_on_spotlight()

    def __dispatch_events_for_load_up_level(self):
        self._event_dispatcher.dispatch_event(EventData(EventCategoryType.CameraManager, EventActionType.GameCamera))
        self._event_dispatcher.dispatch_event(EventData(EventCategoryType.CameraManager, EventActionType.SetCameraTarget, [Application.Player]))
        self._event_dispatcher.dispatch_event(EventData(EventCategoryType.CollisionManager, EventActionType.TurnOnCollisionDetection))
        self._event_dispatcher.dispatch_event(EventData(EventCategoryType.RendererManager, EventActionType.IsGame))

    def __set_up_teleporter(self):
        Application.ActiveScene.remove(Application.Player)

    def __check_pause_menu(self):
        if Application.ActiveScene.name == GameConstants.Scene.EARTH \
                or Application.ActiveScene.name == GameConstants.Scene.MARS \
                or Application.ActiveScene.name == GameConstants.Scene.SATURN \
                or Application.ActiveScene.name == GameConstants.Scene.HOUSE:
            if self.__input_handler.is_tap(pygame.K_ESCAPE, 100):
                self._event_dispatcher.dispatch_event(EventData(EventCategoryType.SceneManager, EventActionType.PauseMenuScene))

    def update(self, game_time):
        self.__check_pause_menu()
        self.__input_handler.update()
        self.__handle_level_complete()
        self.__handle_all_levels_complete()

        enemy_text = f"Enemies count: {self.__enemies_in_scene_count}"

        if self.__enemies_in_scene_count == GameConstants.DEFAULT_ENEMIES:
            enemy_text = f"Enemies count: {0}"

        GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,[enemy_text, GameConstants.UITextPrompts.UI_TEXT_ENEMY_COUNT]))

    def __load_level(self):
        self.__dispatch_events_for_load_up_level()

    def __check_turn_on_spotlight(self):
        if Application.ActiveScene.name is GameConstants.Scene.MARS:
            self._event_dispatcher.dispatch_event(EventData(EventCategoryType.RendererManager, EventActionType.TurnSpotLightOn))

    def __handle_level_complete(self):
        if self.__enemies_in_scene_count <= 0:
            self.__level_complete = True
            if Application.ActiveScene.name is GameConstants.Scene.EARTH or Application.ActiveScene.name is GameConstants.Scene.HOUSE:
                Application.EarthComplete = True
            if Application.ActiveScene.name is GameConstants.Scene.MARS:
                Application.MarsComplete = True
            if Application.ActiveScene.name is GameConstants.Scene.SATURN:
                Application.SaturnComplete = True

            self.__enemies_in_scene_count = GameConstants.DEFAULT_ENEMIES

            if Application.EarthComplete and Application.MarsComplete and Application.SaturnComplete:
                self._event_dispatcher.dispatch_event(
                    EventData(EventCategoryType.SceneManager, EventActionType.EndLevelScene,
                              [GameConstants.Menu.END_LEVEL_COMPLETE_MENU]))

    def __handle_all_levels_complete(self):
        if self.__level_complete:
            self._event_dispatcher.dispatch_event(EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,["Press E around the teleporter to save another planet!", GameConstants.UITextPrompts.UI_TEXT_BOTTOM]))
