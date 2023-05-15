
import pygame

class InputHandler:
    def __init__(self):
        self.__keys = pygame.key.get_pressed()
        self.__last_keys = self.__keys
        self.__last_keypress_time = 0

    def update(self):
        self.__last_keys = self.__keys
        self.__keys = pygame.key.get_pressed()

    def __is_pressed(self, key):
        return self.__keys[key]

    def is_released(self, key):
        return not self.__keys[key]

    def __was_just_pressed(self, key):
        if self.__keys[key] and not self.__last_keys[key]:
            self.last_keypress_time = pygame.time.get_ticks()
            return True
        else:
            return False

    def is_tap(self, key, tap_threshold):
        if self.__is_pressed(key):
            return True
        return self.__was_just_pressed(key) and pygame.time.get_ticks() - self.__last_keypress_time < tap_threshold



