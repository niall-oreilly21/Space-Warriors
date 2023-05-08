from Engine.Components.Component import Component
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Other.InputHandler import InputHandler
from Engine.Other.Interfaces.MovementInterface import MovementInterface
import pygame

from Engine.Other.Transform2D import Direction
from Engine.Time.GameTime import GameTime


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
        print(game_time.elapsed_time)
        if self.input_handler.is_tap(pygame.K_LEFT, self.tap_threshold):
                self.parent.get_component(SpriteRenderer2D).flip_x = True
                self.transform.translate_by(Direction.LEFT * self.speed_x * game_time.elapsed_time)

    def move_right(self, game_time):
        if self.input_handler.is_tap(pygame.K_RIGHT, self.tap_threshold):
            self.parent.get_component(SpriteRenderer2D).flip_x = False
            self.transform.translate_by(Direction.RIGHT * self.speed_x * game_time.elapsed_time)

    def move_up(self, game_time):
        if self.input_handler.is_tap(pygame.K_UP, self.tap_threshold):
                self.parent.get_component(SpriteRenderer2D).flip_y = True
                self.transform.translate_by(Direction.UP * self.speed_y * game_time.elapsed_time)

    def move_down(self, game_time):
        if self.input_handler.is_tap(pygame.K_DOWN, self.tap_threshold):
                self.parent.get_component(SpriteRenderer2D).flip_y = False
                self.transform.translate_by(Direction.DOWN * self.speed_y * game_time.elapsed_time)
