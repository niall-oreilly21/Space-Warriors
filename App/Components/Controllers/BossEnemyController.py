from App.Components.Controllers.EnemyController import EnemyController
from App.Constants.Application import Application
from App.Constants.GameConstants import GameConstants


class BossEnemyController(EnemyController):
    def __init__(self, name, target, speed, min_distance_to_target, min_distance_to_stop_firing, gun):
        super().__init__(name, target, speed, min_distance_to_target)
        self.__gun = gun
        self.__min_distance_to_stop_firing = min_distance_to_stop_firing

    def start(self):
        super().start()

    def update(self, game_time):
        super().update(game_time)

    def _follow_target(self):
        super()._follow_target()

        if self._distance_from_target >= self.__min_distance_to_stop_firing:
            self.__gun.fire(self._direction)

    def _kill_enemy(self):
        Application.ActiveScene.remove(self.__gun)

        super()._kill_enemy()


    def clone(self):
        return BossEnemyController(self.name, self._target, self._speed, self._min_distance_to_target, self.__min_distance_to_stop_firing, self.__gun)