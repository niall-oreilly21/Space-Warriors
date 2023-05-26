from pygame import Vector2
from Engine.GameObjects.Components.Cameras.Camera import Camera
from Engine.GameObjects.Components.Component import Component

class ThirdPersonController(Component):
    def __init__(self, name, target):
        super().__init__(name)
        self.__target = target
        self.__transition_speed = 0.01  # Adjust the speed of the transition as desired
        self.__smooth_position = None
        self.__camera = None
        
    def start(self):
        self.__camera = self.parent.get_component(Camera)

    def update(self, game_time):
        if self.__target is not None:
            camera_component = self.parent.get_component(Camera)
            if camera_component is not None:
                viewport_center = Vector2(self.__camera.viewport.x / 2, self.__camera.viewport.y / 2)
                target_position = self.__target.transform.position - viewport_center

                if self.__smooth_position is None:
                    # Start the smooth transition from the current camera position
                    self.__smooth_position = self._transform.position

                # Calculate the transition distance based on elapsed time
                transition_distance = target_position - self.__smooth_position
                transition_speed = transition_distance * self.__transition_speed * game_time.elapsed_time

                # Apply smooth transition using lerp
                self.__smooth_position += transition_speed

                # Update the camera position
                self._transform.position = self.__smooth_position




