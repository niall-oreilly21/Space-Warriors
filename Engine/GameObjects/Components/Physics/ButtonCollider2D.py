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

    def button_pressed(self):

        Constants.EVENT_DISPATCHER.dispatch_event(
            EventData(EventCategoryType.SceneManager, EventActionType.ExitGame))

        if self._parent.name.lower() == "main menu button":
            Constants.EVENT_DISPATCHER.dispatch_event(EventData(EventCategoryType.SceneManager, EventActionType.MainMenuScene))

    def update(self, game_time):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        if self.camera_manager.active_camera.parent.get_component(ThirdPersonController):
            mouse_pos =  mouse_pos + self.camera_manager.active_camera.transform.position

        if self.bounds.collidepoint(mouse_pos) and mouse_buttons[0]:
            self.button_pressed()


    def draw(self, screen, camera_manager):
        super().draw(screen, camera_manager)
        # Additional drawing logic for buttons can be added here, if needed
