from Engine.GameObjects.Components.Component import Component
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D


class PetController(Component):
    def __init__(self, name, target_object, speed):
        super().__init__(name)
        self.__animator = None
        self.__rend = None
        self.__target_object = target_object
        self.__speed = speed
        self.__rigidbody = None

    def start(self):
        self.__rend = self._parent.get_component(SpriteRenderer2D)
        self.__animator = self._parent.get_component(SpriteAnimator2D)
        self.__rigidbody = self._parent.get_component(Rigidbody2D)

    def update(self, game_time):
        target_position = self.__target_object.transform.position
        current_position = self._transform.position

        # Calculate the direction vector towards the target
        direction = target_position - current_position

        # Normalize the direction vector
        if direction.length() > 0:
            direction.normalize()

        desired_position = target_position - direction * 20

        # Calculate the movement amount based on speed and elapsed time
        movement_amount = self.__rigidbody.velocity = direction * self.__speed * 0.0001

        # Calculate the distance to the desired position
        distance_to_desired = desired_position - current_position

        # Check if the pet is already at the desired position or too close
        if distance_to_desired.length() <= movement_amount.length():
            # Move the pet directly to the desired position
            self._transform.position = desired_position
        else:
            # Move the pet by the movement amount
            self._transform.position += movement_amount
