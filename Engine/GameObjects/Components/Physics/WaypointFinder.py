from Engine.GameObjects.Components.Component import Component
import math


class WaypointFinder(Component):
    def __init__(self, name, waypoints):
        super().__init__(name)
        self.waypoints = waypoints
        self.current_waypoint = 0
        self.direction = 1  # 1 for forward, -1 for backward

    def get_current_waypoint(self):
        return self.waypoints[self.current_waypoint]

    def move_to_next_waypoint(self):
        self.current_waypoint += self.direction

        # Check if reached the end of the path
        if self.current_waypoint >= len(self.waypoints):
            self.current_waypoint = len(self.waypoints) - 2
            self.direction = -1
        # Check if reached the beginning of the path
        elif self.current_waypoint < 0:
            self.current_waypoint = 1
            self.direction = 1

    def has_reached_waypoint(self, enemy_position, distance_threshold=10):
        current_waypoint = self.get_current_waypoint()
        distance = math.sqrt(
            (current_waypoint[0] - enemy_position[0]) ** 2 + (current_waypoint[1] - enemy_position[1]) ** 2)

        return distance <= distance_threshold

    def lerp(self, start, end, t):
        return start + (end - start) * t

    def clone(self):
        return WaypointFinder(self.name, self.waypoints)



