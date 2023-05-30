import pygame

from App.Constants.Constants import Constants
from Engine.GameObjects.Components.Cameras.ThirdPersonController import ThirdPersonController
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType


class ButtonCollider2D(BoxCollider2D):
    def __init__(self, name, event_handler, camera_manager, anchor=pygame.Vector2(0, 0)):
        super().__init__(name, anchor)
        self.event_handler = event_handler
        self.camera_manager = camera_manager
        self._mouse_position = None

    def start(self):
        super().start()

    def update(self, game_time):
        self._mouse_position = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        if self.bounds.collidepoint(self._mouse_position) and mouse_buttons[0]:
            self.button_pressed()

    def draw(self, screen, camera_manager):
        super().draw(screen, camera_manager)

    def button_pressed(self):
        if self._parent.name == Constants.Button.START_BUTTON:
            Constants.EVENT_DISPATCHER.dispatch_event(
                EventData(EventCategoryType.SceneManager, EventActionType.LevelScene))
        elif self._parent.name == Constants.Button.QUIT_BUTTON:
            Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                EventActionType.ExitGame))
        elif self._parent.name == Constants.Button.RESUME_BUTTON:
            Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                EventActionType.GameScene))
        elif self._parent.name == Constants.Button.MAIN_MENU_BUTTON:
            Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                EventActionType.MainMenuScene))
        elif self._parent.name == Constants.Button.EARTH_BUTTON:
            Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager,
                                                                EventActionType.GameScene))
