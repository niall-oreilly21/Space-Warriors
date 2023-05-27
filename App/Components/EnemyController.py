from pygame import Vector2
import math

from Engine.Other.Enums.GameObjectEnums import GameObjectEnemyType
from Engine.GameObjects.Components.Component import Component
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Other.Enums.ActiveTake import ActiveTake


class EnemyController(Component):
    def __init__(self, name, target_object, speed, enemy_type):
        super().__init__(name)
        self.__animator = None
        self.__rend = None
        self.__target_object = target_object
        self.__speed = speed
        self.__type = enemy_type

    def start(self):
        self.__rend = self._parent.get_component(SpriteRenderer2D)
        self.__animator = self._parent.get_component(SpriteAnimator2D)

    def update(self, game_time):
        target_position = self.__target_object.transform.position
        enemy_position = self.transform.position

        target_position = self.__target_object.transform.position
        enemy_position = self.transform.position

        direction = target_position - enemy_position
        direction.normalize()

        angle = math.degrees(math.atan2(direction.y, direction.x))
        if angle < 0:
            angle += 360

        if 45 <= angle < 135:
            movement_direction = "down"
        elif 135 <= angle < 225:
            movement_direction = "left"
        elif 225 <= angle < 315:
            movement_direction = "up"
        else:
            movement_direction = "right"

        self.transform.position += direction * game_time.elapsed_time * 0.001 * self.__speed

        if movement_direction == "right":
            self.__rend.flip_x = False
            self.__animator.set_active_take(self.move_x_active_take())
        elif movement_direction == "left":
            self.__rend.flip_x = True
            self.__animator.set_active_take(self.move_x_active_take())
        elif movement_direction == "up":
            self.__animator.set_active_take(self.move_up_active_take())
        elif movement_direction == "down":
            self.__animator.set_active_take(self.move_down_active_take())

    def move_x_active_take(self):
        if self.__type == GameObjectEnemyType.Rat:
            return ActiveTake.ENEMY_RAT_MOVE_X
        elif self.__type == GameObjectEnemyType.Wolf:
            return ActiveTake.ENEMY_WOLF_MOVE_X
        else:
            return ActiveTake.ENEMY_ALIEN_MOVE_X

    def move_up_active_take(self):
        if self.__type == GameObjectEnemyType.Rat:
            return ActiveTake.ENEMY_RAT_MOVE_UP
        elif self.__type == GameObjectEnemyType.Wolf:
            return ActiveTake.ENEMY_WOLF_MOVE_UP
        else:
            return ActiveTake.ENEMY_ALIEN_MOVE_UP

    def move_down_active_take(self):
        if self.__type == GameObjectEnemyType.Rat:
            return ActiveTake.ENEMY_RAT_MOVE_DOWN
        elif self.__type == GameObjectEnemyType.Wolf:
            return ActiveTake.ENEMY_WOLF_MOVE_DOWN
        else:
            return ActiveTake.ENEMY_ALIEN_MOVE_DOWN
