import pygame

from App.Constants.Application import Application
from App.Constants.GameConstants import GameConstants
from Engine.GameObjects.Components.Physics.Collider import Collider
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType


class HouseCollider(Collider):

    def __init__(self, name, scene_event_action_type):
        self.__scene_event_action_type = scene_event_action_type
        super().__init__(name)

    def handle_response(self, colliding_game_object):
        if colliding_game_object == Application.Player:
            GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager, self.__scene_event_action_type))

    def clone(self):
        return HouseCollider(self.name, self.__scene_event_action_type)

    def handle_collision_exit(self):
        GameConstants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.GameStateManager, EventActionType.SetUITextHelper,["", GameConstants.UITextPrompts.UI_TEXT_BOTTOM]))