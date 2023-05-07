from Component import Component
from Sprite import Sprite


class SpriteAnimator2D(Component):
    def __init__(self, name, frame_rects, material, fps=10):
        super().__init__(name)
        self.frame_rects = frame_rects
        self.material = material
        self.fps = fps
        self.current_frame = 0
        self.elapsed_time = 0  # Initialize elapsed_time to 0

    def update(self, game_time):
        # Calculate the duration of each frame in milliseconds
        frame_duration = 1000 / self.fps

        # Add the elapsed time to the animation timer
        self.elapsed_time += game_time.get_elapsed_game_time()

        # If the animation timer exceeds the frame duration, advance to the next frame
        if self.elapsed_time >= frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frame_rects)
            self.elapsed_time -= frame_duration

        # Set the current sprite on the material
        self.material.source_rect = self.frame_rects[self.current_frame]

    def get_current_sprite(self):
        return Sprite(self.material.texture, self.frame_rects[self.current_frame], self.material.color)

    def set_fps(self, fps):
        self.fps = fps


