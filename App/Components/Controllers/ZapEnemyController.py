from App.Components.Controllers.EnemyController import EnemyController
from App.Constants.GameConstants import GameConstants
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType


class ZapEnemyController(EnemyController):
    def __init__(self, name, target, speed, min_distance_to_target, zap_speed_multiplier, zap_interval=2):
        super().__init__(name, target, speed, min_distance_to_target)
        self.__zap_speed_multiplier = zap_speed_multiplier
        self.__total_elapsed_time = 0
        self.__zap_interval = zap_interval * 1000
        self.__initial_speed = speed

    def start(self):
        super().start()

    def update(self, game_time):
        super().update(game_time)
        self._speed = self.__initial_speed

        self.__total_elapsed_time += game_time.elapsed_time

        if self.__total_elapsed_time >= self.__zap_interval:
            GameConstants.EVENT_DISPATCHER.dispatch_event(
                EventData(EventCategoryType.SoundManager, EventActionType.PlaySound,
                          [GameConstants.Music.ZAP_SOUND, None]))
            self._speed *= self.__zap_speed_multiplier
            self.__total_elapsed_time = 0

    def clone(self):
        return ZapEnemyController(self.name, self._target, self._speed, self._min_distance_to_target, self.__zap_speed_multiplier, self.__zap_interval)
