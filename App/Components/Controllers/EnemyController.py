from pygame import Vector2
import math

from App.Constants.Application import Application
from App.Constants.GameConstants import GameConstants
from Engine.GameObjects.Components.FollowController import FollowController
from Engine.GameObjects.Components.Physics.WaypointFinder import WaypointFinder
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType
from Engine.Other.Enums.GameObjectEnums import GameObjectCategory, GameObjectDirection
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Other.Enums.ActiveTake import ActiveTake


class EnemyController(FollowController):
    def __init__(self, name, target, speed, min_distance_to_target):
        super().__init__(name, target)
        self.__waypoint_finder = None
        self.__way_point_system = None
        self.__animator = None
        self.__rend = None
        self.__target = target
        self._speed = speed
        self.__rigidbody = None
        self._min_distance_to_target = min_distance_to_target
        self._direction = 0
        self._distance_from_target = 0
        self.__position = None
        self.__target_position = None

    def start(self):
        self.__rend = self._parent.get_component(SpriteRenderer2D)
        self.__animator = self._parent.get_component(SpriteAnimator2D)
        self.__rigidbody = self._parent.get_component(Rigidbody2D)
        self.__waypoint_finder = self._parent.get_component(WaypointFinder)

    def update(self, game_time):
        self.__check_enemy_health()
        self.__target_position = self.__target.transform.position
        self.__position = self.transform.position

        self._distance_from_target = math.sqrt(
            (self.__target_position.x - self.__position.x) ** 2 + (self.__target_position.y - self.__position.y) ** 2)

        if self._distance_from_target <= self._min_distance_to_target:
            self._follow_target()

        else:
            if self.__waypoint_finder is not None:
                self.calculate_patrol_routes(game_time)

    def __check_enemy_health(self):
        if self.parent.health <= 0:
            self.parent.health = 0
            Application.ActiveScene.remove(self.parent.health_bar)
            Application.ActiveScene.remove(self.parent)
            GameConstants.EVENT_DISPATCHER.dispatch_event(
                EventData(EventCategoryType.SoundManager, EventActionType.PlaySound,
                          [GameConstants.Music.ENEMY_DEATH_SOUND, False]))
            GameConstants.EVENT_DISPATCHER.dispatch_event(
                EventData(EventCategoryType.GameStateManager, EventActionType.RemoveEnemyFromScene)
            )

    def _follow_target(self):
        self.calculate_movement_direction(self.__target.transform.position, self.transform.position)

    def calculate_patrol_routes(self, game_time):

        # Player is out of range, follow the waypoint path
        if self.__waypoint_finder.has_reached_waypoint(self.__position):
            self.__waypoint_finder.move_to_next_waypoint()

        # Calculate the interpolation factor based on the distance to the current waypoint
        current_waypoint = self.__waypoint_finder.get_current_waypoint()
        total_distance = math.sqrt(
            (current_waypoint[0] - self.__position.x) ** 2 + (current_waypoint[1] - self.__position.y) ** 2)

        t = min(1, self._speed * game_time.elapsed_time * 0.009 / total_distance)

        t = min(t, 1)

        self.calculate_movement_direction(current_waypoint, self.__position)

        self._direction = current_waypoint - self.__position
        self._direction.normalize()
        target_velocity = self._direction * self._speed * 0.01

        current_velocity = Vector2(0, 0)

        # Interpolate between the current velocity and the target velocity
        new_velocity = Vector2.lerp(current_velocity, target_velocity, t)

        self.__rigidbody.velocity = new_velocity

    def calculate_movement_direction(self, target_position, enemy_position):
        self._direction = target_position - enemy_position

        if self._direction.x > 0 and self._direction.y > 0:
            self._direction.normalize()

        angle = math.degrees(math.atan2(self._direction.y, self._direction.x))
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

        self.__rigidbody.velocity = self._direction * self._speed * 0.0001

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
        return EnemyController(self.name, self.__target, self._speed, self._min_distance_to_target)
