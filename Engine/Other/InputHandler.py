
import pygame

class InputHandler:
    def __init__(self):
        self.keys = pygame.key.get_pressed()
        self.last_keys = self.keys
        self.last_keypress_time = 0

    def update(self):
        self.last_keys = self.keys
        self.keys = pygame.key.get_pressed()

    def is_pressed(self, key):
        return self.keys[key]

    def is_released(self, key):
        return not self.keys[key]

    def was_just_pressed(self, key):
        if self.keys[key] and not self.last_keys[key]:
            self.last_keypress_time = pygame.time.get_ticks()
            return True
        else:
            return False

    def is_tap(self, key, tap_threshold):
        if self.is_pressed(key):
            return True
        return self.was_just_pressed(key) and pygame.time.get_ticks() - self.last_keypress_time < tap_threshold



