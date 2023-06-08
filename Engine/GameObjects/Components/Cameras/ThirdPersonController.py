from pygame import Vector2

from App.Constants.Application import Application
from Engine.GameObjects.Components.Cameras.Camera import Camera
from Engine.GameObjects.Components.Component import Component
from Engine.GameObjects.Components.FollowController import FollowController


class ThirdPersonController(FollowController):
    def __init__(self, name, target):
        super().__init__(name, target)
        self.__smoothness = 0.5  # Adjust the smoothness factor (0.0 to 1.0)
        self.__smooth_position = None
        self.__camera = None

    def start(self):
        self.__camera = self.parent.get_component(Camera)

    def update(self, game_time):
        if self._target is not None:
            camera_component = self.parent.get_component(Camera)
            if camera_component is not None:
                viewport_center = Vector2(Application.ActiveCamera.viewport.x / 2, Application.ActiveCamera.viewport.y / 2)
                target_position = self._target.transform.position - viewport_center

                if self.__smooth_position is None:
                    # Start the smooth transition from the current camera position
                    self.__smooth_position = self._transform.position

                # Calculate the interpolation factor based on smoothness and elapsed time
                smoothness_factor = 1 - pow(1 - self.__smoothness, game_time.elapsed_time)

                # Interpolate between the current camera position and the target position
                self.__smooth_position = Vector2.lerp(self.__smooth_position, target_position, smoothness_factor)

                # Update the camera position
                self._transform.position = self.__smooth_position

    def clone(self):
        return ThirdPersonController(self._name, self._target)
