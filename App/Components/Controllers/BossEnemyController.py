from App.Components.Controllers.EnemyController import EnemyController


#Shoots bullets
#Can zap speed

class BossEnemyController(EnemyController):
    def __init__(self, name, target_object, speed, min_distance, gun):
        super().__init__(name, target_object, speed, min_distance)
        self._gun = gun

    def start(self):
        super().start()

    def update(self, game_time):
        super().update(game_time)

        self._gun.fire(self._direction)

    def clone(self):
        return EnemyController(self.name, self.__target_object, self.__speed, self.__min_distance)