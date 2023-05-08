import pygame

class GameTime:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.last_tick = 0
        self.elapsed_time = 0
        self.total_time = 0

    def tick(self):
        now = pygame.time.get_ticks()
        self.elapsed_time = now - self.last_tick
        self.last_tick = now
        self.total_time = now - self.start_time

    def fps(self):
        return self.clock.get_fps()

    def limit_fps(self, fps_limit):
        self.clock.tick(fps_limit)