from App.Components.Controllers.EnemyController import EnemyController

class BossEnemyController(EnemyController):
    def __init__(self, name, target, speed, min_distance_to_target, min_distance_to_stop_firing, gun):
        super().__init__(name, target, speed, min_distance_to_target)
        self._gun = gun
        self.__min_distance_to_stop_firing = min_distance_to_stop_firing

    def start(self):
        super().start()

    def update(self, game_time):
        super().update(game_time)

    def _follow_target(self):
        super()._follow_target()

        if self._distance_from_target >= self.__min_distance_to_stop_firing:
            self._gun.fire(self._direction)


    def clone(self):
        return BossEnemyController(self.name, self._target, self._speed, self._min_distance_to_target, self.__min_distance_to_stop_firing, self._gun)