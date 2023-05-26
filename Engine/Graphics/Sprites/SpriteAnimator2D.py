from Engine.GameObjects.Components.Component import Component
from Engine.Graphics.Sprites.Take import Take
from Engine.Graphics.Sprites.Sprite import Sprite


class ActiveTake:
    pass


class SpriteAnimator2D(Component):
    def __init__(self, name, animator_info, material, active_take, fps):
        super().__init__(name)
        self.__animator_info = animator_info
        self.__current_frames = None
        self.__active_take = None
        self.set_active_take(active_take)
        self.__material = material
        self.__fps = fps
        self.__current_frame = 0
        self.__elapsed_time = 0



    def update(self, game_time):

        if self.__active_take is None:
            pass

        # Calculate the duration of each frame in milliseconds
        frame_duration = 1000 / self.__fps
        # Add the elapsed time to the animation timer
        self.__elapsed_time += game_time.elapsed_time

        # If the animation timer exceeds the frame duration, advance to the next frame
        if self.__elapsed_time >= frame_duration:
            self.__current_frame = (self.__current_frame + 1) % len(self.__current_frames)
            self.__elapsed_time -= frame_duration

        # Set the current sprite on the material
        self.__material.source_rect = self.__current_frames[self.__current_frame]

    def set_active_take(self, active_take):
        for animator_info in self.__animator_info:
            if animator_info.active_take == active_take:
                self.__current_frames = animator_info.frame_rects
                self.__active_take = active_take


    def get_current_sprite(self):
        return Sprite(self.__material.texture, self.__current_frames[self.__current_frame], self.__material.color)




