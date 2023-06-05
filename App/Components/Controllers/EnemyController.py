from pygame import Vector2
import math

from Engine.GameObjects.Components.Physics.WaypointFinder import WaypointFinder
from Engine.Other.Enums.GameObjectEnums import GameObjectCategory, GameObjectDirection
from Engine.GameObjects.Components.Component import Component
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Other.Enums.ActiveTake import ActiveTake


class EnemyController(Component):
    def __init__(self, name, target_object, speed, min_distance):
        super().__init__(name)
        self.__waypoint_finder = None
        self.__way_point_system = None
        self.__animator = None
        self.__rend = None
        self.__target_object = target_object
        self.__speed = speed
        self.__rigidbody = None
        self.__min_distance = min_distance

    def start(self):
        self.__rend = self._parent.get_component(SpriteRenderer2D)
        self.__animator = self._parent.get_component(SpriteAnimator2D)
        self.__rigidbody = self._parent.get_component(Rigidbody2D)
        self.__waypoint_finder = self._parent.get_component(WaypointFinder)


    def update(self, game_time):
        target_position = self.__target_object.transform.position
        enemy_position = self.transform.position

        distance = math.sqrt((target_position.x - enemy_position.x) ** 2 + (target_position.y - enemy_position.y) ** 2)

        if distance <= 10:
            pass
            #self.calculate_movement_direction(target_position,enemy_position)
        else:
            if self.__waypoint_finder is not None:
                # Enemy is outside the desired range, so it remains stationary
                self.calculate_patrol_routes(enemy_position, game_time)

    def calculate_patrol_routes(self, enemy_position, game_time):
        # Player is out of range, follow the waypoint path
        if self.__waypoint_finder.has_reached_waypoint(enemy_position):
            self.__waypoint_finder.move_to_next_waypoint()

        # Calculate the interpolation factor based on the distance to the current waypoint
        current_waypoint = self.__waypoint_finder.get_current_waypoint()
        total_distance = math.sqrt(
            (current_waypoint[0] - enemy_position.x) ** 2 + (current_waypoint[1] - enemy_position.y) ** 2)


        t = min(1, self.__speed * game_time.elapsed_time * 0.009 / total_distance)

        # Clamp t to a maximum of 1
        t = min(t, 1)
        # Ensure t doesn't exceed 1

        self.calculate_movement_direction(current_waypoint, enemy_position)

        # Calculate the new velocity for the enemy
        direction = current_waypoint - enemy_position
        direction.normalize()
        target_velocity = direction * self.__speed * 0.01

        # Convert self.__rigidbody.velocity to a Vector2 object
        current_velocity = Vector2(0, 0)

        # Interpolate between the current velocity and the target velocity
        new_velocity = Vector2.lerp(current_velocity, target_velocity, t)

        # Set the new velocity for the enemy
        self.__rigidbody.velocity = new_velocity

    def calculate_movement_direction(self, target_position, enemy_position):
        direction = target_position - enemy_position
        direction.normalize()

        angle = math.degrees(math.atan2(direction.y, direction.x))
        if angle < 0:
            angle += 360

        if 45 <= angle < 135:
            movement_direction = GameObjectDirection.Down
        elif 135 <= angle < 225:
            movement_direction = GameObjectDirection.Left
        elif 225 <= angle < 315:
            movement_direction = GameObjectDirection.Up
        else:
            movement_direction = GameObjectDirection.Right

        self.__rigidbody.velocity = self.__speed * 0.0001

        if movement_direction == GameObjectDirection.Right:
            self.__rend.flip_x = False
            self.__animator.set_active_take(self.move_x_active_take())
        elif movement_direction == GameObjectDirection.Left:
            self.__rend.flip_x = True
            self.__animator.set_active_take(self.move_x_active_take())
        elif movement_direction == GameObjectDirection.Up:
            self.__animator.set_active_take(self.move_up_active_take())
        elif movement_direction == GameObjectDirection.Down:
            self.__animator.set_active_take(self.move_down_active_take())

    def move_x_active_take(self):
        if self.parent.game_object_category == GameObjectCategory.Rat:
            return ActiveTake.ENEMY_RAT_MOVE_X
        elif self.parent.game_object_category == GameObjectCategory.Wolf:
            return ActiveTake.ENEMY_WOLF_MOVE_X
        else:
            return ActiveTake.ENEMY_ALIEN_MOVE_X

    def move_up_active_take(self):
        if self.parent.game_object_category == GameObjectCategory.Rat:
            return ActiveTake.ENEMY_RAT_MOVE_UP
        elif self.parent.game_object_category == GameObjectCategory.Wolf:
            return ActiveTake.ENEMY_WOLF_MOVE_UP
        else:
            return ActiveTake.ENEMY_ALIEN_MOVE_UP

    def move_down_active_take(self):
        if self.parent.game_object_category == GameObjectCategory.Rat:
            return ActiveTake.ENEMY_RAT_MOVE_DOWN
        elif self.parent.game_object_category == GameObjectCategory.Wolf:
            return ActiveTake.ENEMY_WOLF_MOVE_DOWN
        else:
            return ActiveTake.ENEMY_ALIEN_MOVE_DOWN

    def clone(self):
        return EnemyController(self.name, self.__target_object, self.__speed)
