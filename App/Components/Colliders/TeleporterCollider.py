import pygame

from App.Constants.Application import Application
from App.Constants.Constants import Constants
from Engine.GameObjects.Components.Physics.Collider import Collider
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType


class TeleporterCollider(Collider):

    def __init__(self, name):
        super().__init__(name)
        self.__rb = None
        self.__target_object = None
        self.__current_path = []
        self.__colliding_game_object = None
        self.__enemy_controller = None

    def start(self):
        pass

    def handle_response(self, colliding_game_object):

        if colliding_game_object == Application.Player:
            Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper, ["Press E to teleport"]))
            self.__check_teleporter_input()

    def handle_collision_exit(self):
        Constants.EVENT_DISPATCHER.dispatch_event(
            EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper, [""]))

    def __check_teleporter_input(self):
        if Application.ActiveScene.name == Constants.Scene.EARTH \
                or Application.ActiveScene.name == Constants.Scene.MARS \
                or Application.ActiveScene.name == Constants.Scene.SATURN:
            if Constants.INPUT_HANDLER.is_tap(pygame.K_e, 100):
                Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.GameStateManager, EventActionType.TurnOnTeleporter))



