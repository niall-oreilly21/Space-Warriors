import math


class CollisionArea:
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height

        def set_x(self, x):
            self.x = x

        def set_y(self, y):
            self.y = y

        def intersects_screen(self, range_rect):
            return (
                    self.x + self.width > range_rect.x - range_rect.width
                    and self.x < range_rect.x + range_rect.width
                    and self.y + self.height > range_rect.y - range_rect.height
                    and self.y < range_rect.y + range_rect.height
            )

        def is_in_range(self, rect_one, rect_two, range_distance):
            center1 = rect_one.center
            center2 = rect_two.center
            distance = math.hypot(center2[0] - center1[0], center2[1] - center1[1])
            return distance <= range_distance
