import pygame

from App.Constants.Application import Application
from App.Constants.GameConstants import GameConstants
from Engine.GameObjects.Components.Physics.Collider import Collider
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType


class HouseCollider(Collider):

    def __init__(self, name):
        super().__init__(name)


    def handle_response(self, colliding_game_object):
        if colliding_game_object == Application.Player:
            GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper, ["Press E to enter the house", GameConstants.UITextPrompts.UI_TEXT_BOTTOM]))
            self.__check_house_open()

    def __check_house_open(self):
            if GameConstants.INPUT_HANDLER.is_tap(pygame.K_e, 100):
                GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager, EventActionType.HouseScene))

    def clone(self):
        return HouseCollider(self.name)

    def handle_collision_exit(self):
        GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,["", GameConstants.UITextPrompts.UI_TEXT_BOTTOM]))