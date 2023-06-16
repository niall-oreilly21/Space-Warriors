from Engine.GameObjects.Components.Component import Component
from Engine.Graphics.Sprites.Sprite import Sprite


class SpriteAnimator2D(Component):
    def __init__(self, name, animator_info, material, active_take, fps):
        super().__init__(name)
        self.__repeat_count = None
        self.__is_animation_complete = None
        self.__is_infinite = None
        self.__animator_info = animator_info
        self.__current_frames = None
        self.__active_take = None
        self.__material = material
        self.__fps = fps
        self.__current_frame = 0
        self.__elapsed_time = 0
        self.set_active_take(active_take)

    @property
    def fps(self):
        return self.__fps

    @fps.setter
    def fps(self, fps):
        self.__fps = fps

    @property
    def material(self):
        return self.__material

    @material.setter
    def material(self, material):
        self.__material = material

    @property
    def animator_info(self):
        return self.__animator_info

    @property
    def active_take(self):
        return self.__active_take

    @property
    def is_animation_complete(self):
        return self.__is_animation_complete

    @property
    def is_infinite(self):
        return self.__is_infinite

    @is_infinite.setter
    def is_infinite(self, is_infinite):
        self.__is_infinite = is_infinite

    def get_current_sprite(self):
        if self.__current_frame < len(self.__current_frames):
            return Sprite(self.__material.texture, self.__current_frames[self.__current_frame], self.__material.color)
        else:
            return Sprite(self.__material.texture, self.__current_frames[0], self.__material.color)

    def set_active_take(self, active_take):
        for animator_info in self.__animator_info:
            if animator_info.active_take == active_take:
                self.__current_frames = animator_info.frame_rects
                self.__active_take = active_take
                self.__is_infinite = animator_info.is_infinite
                self.__is_animation_complete = False
                self.__repeat_count = animator_info.repeat_count


    def update(self, game_time):
        if self.__active_take is None:
            return

        # Calculate the duration of each frame in milliseconds
        frame_duration = 1000 / self.__fps
        # Add the elapsed time to the animation timer
        self.__elapsed_time += game_time.elapsed_time

        # Set the current sprite on the material
        if self.__current_frame < len(self.__current_frames):
            self.__material.source_rect = self.__current_frames[self.__current_frame]
        else:
            self.__material.source_rect = self.__current_frames[0]

        # If the animation timer exceeds the frame duration, advance to the next frame
        if self.__elapsed_time >= frame_duration:
            self.__current_frame = (self.__current_frame + 1) % len(self.__current_frames)
            self.__elapsed_time -= frame_duration

            # Check if the animation has reached the end
            if self.__current_frame == 0:
                if not self.__is_infinite:

                    if self.__repeat_count <= 1:

                        # Animation completed the desired repeat count, set the animation complete flag
                        self.__is_animation_complete = True
                        self.__active_take = None
                    else:
                        # Animation still needs to be repeated, decrement the repeat count
                        self.__repeat_count -= 1
                        self.__current_frame = 0
                        self.__elapsed_time = 0

    def clone(self):
        clone_animator_info = [take.clone() for take in self.__animator_info]
        return SpriteAnimator2D(self._name, clone_animator_info, self.__material.clone(), self.__active_take,
                                self.__fps)
