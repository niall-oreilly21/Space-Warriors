from pygame import Vector2
from Engine.GameObjects.Components.Component import Component

class Rigidbody2D(Component):
    def __init__(self, name, mass=1.0, drag=0.0):
        super().__init__(name)
        self.__mass = mass
        self.__drag = drag
        self.__velocity = Vector2(0, 0)
        self.__acceleration = Vector2(0, 0)
        self.__time_scale = 0.001  # Time scaling factor for velocity and acceleration

    @property
    def mass(self):
        return self.__mass

    @property
    def velocity(self):
        return self.__velocity

    @velocity.setter
    def velocity(self, velocity):
        self.__velocity = velocity

    @mass.setter
    def mass(self, value):
        self.__mass = value

    @property
    def drag(self):
        return self.__drag

    @drag.setter
    def drag(self, value):
        self.__drag = value

    def apply_force(self, force):
        self.__acceleration += force / self.__mass

    def update(self, game_time):
        delta_time = game_time.elapsed_time

        # Update velocity using acceleration and drag
        self.__velocity += self.__acceleration * delta_time
        self.__velocity -= self.__velocity * self.__drag * delta_time

        # Update position using velocity
        self._transform.position += self.__velocity * delta_time

    def clone(self):
        return Rigidbody2D(self._name, self.__mass, self.__drag)