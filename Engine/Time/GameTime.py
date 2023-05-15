import pygame

class GameTime:
    def __init__(self):
        self.__clock = pygame.time.Clock()
        self.__start_time = pygame.time.get_ticks()
        self.__last_tick = 0
        self.__elapsed_time = 0
        self.__total_time = 0

    @property
    def elapsed_time(self):
        return self.__elapsed_time

    def tick(self):
        now = pygame.time.get_ticks()
        self.__elapsed_time = now - self.__last_tick
        self.__last_tick = now
        self.__total_time = now - self.__start_time

    def fps(self):
        return self.__clock.get_fps()

    def limit_fps(self, fps_limit):
        self.__clock.tick(fps_limit)