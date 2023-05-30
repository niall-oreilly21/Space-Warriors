import pygame

from Engine.Managers.Manager import Manager
from Engine.Other.Enums.EventEnums import EventCategoryType


class GameStateManager(Manager):
    def __init__(self, event_dispatcher, input_handler):
        super().__init__(event_dispatcher)
        self.__input_handler = input_handler

    def _subscribe_to_events(self):
        self._event_dispatcher.add_listener(EventCategoryType.CameraManager, self._handle_events)

    def _handle_events(self, event_data):
        pass

    def __check_pause_menu(self):
        if self.__input_handler.is_tap(pygame.K_ESCAPE, 100):
            pass
            # self._event_dispatcher.dispatch(EventData(EventCategoryType.SceneManager, Event))

    def update(self, game_time):
        self.__check_pause_menu()
        self.__input_handler.update()
