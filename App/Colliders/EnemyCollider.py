from Engine.GameObjects.Components.Physics.Collider2D import Collider2D
from Engine.Other.Interfaces.IDamageable import IDamageable


class EnemyCollider(Collider2D):

    def __init__(self, name):
        super().__init__(name)

    def handle_response(self, parent_game_object):
        print("I made it")

        if isinstance(parent_game_object, IDamageable):
            parent_game_object.damage(20)

            print(parent_game_object.health)

            if parent_game_object.health <=0:
                print("HI")