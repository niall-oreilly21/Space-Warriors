from Component import Component
from InputHandler import InputHandler
from MovementInterface import MovementInterface
import pygame

from Transform2D import Direction


class PlayerController(Component, MovementInterface):

    def __init__(self, name, speed_x, speed_y):
        super().__init__(name)
        self.input_handler = InputHandler()
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.last_keypress_time = 0
        self.tap_threshold = 200

    def update(self, game_time):
        self.input_handler.update()
        self.move_left(game_time)
        self.move_right(game_time)
        self.move_up(game_time)
        self.move_down(game_time)

    def move_left(self, game_time):
         if self.input_handler.is_tap(pygame.K_LEFT, self.tap_threshold):
                self.transform.translate_by(Direction.LEFT * self.speed_x * game_time.get_elapsed_game_time())

    def move_right(self, game_time):
        if self.input_handler.is_tap(pygame.K_RIGHT, self.tap_threshold):
                self.transform.translate_by(Direction.RIGHT * self.speed_x * game_time.get_elapsed_game_time())

    def move_up(self, game_time):
        if self.input_handler.is_tap(pygame.K_UP, self.tap_threshold):
                self.transform.translate_by(Direction.UP * self.speed_y * game_time.get_elapsed_game_time())

    def move_down(self, game_time):
        if self.input_handler.is_tap(pygame.K_DOWN, self.tap_threshold):
                self.transform.translate_by(Direction.DOWN * self.speed_y * game_time.get_elapsed_game_time())
