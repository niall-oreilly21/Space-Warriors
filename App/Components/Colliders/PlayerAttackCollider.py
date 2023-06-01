import time

from App.Constants.Constants import Constants
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Collider import Collider
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Enums.GameObjectEnums import GameObjectCategory


class PlayerAttackCollider(Collider):

    def __init__(self, name):
        super().__init__(name)

    def handle_response(self, colliding_game_object):
        current_time = time.time()

        # Player and enemy collide
        if colliding_game_object.game_object_category == GameObjectCategory.Alien or \
                colliding_game_object.game_object_category == GameObjectCategory.Wolf or \
                colliding_game_object.game_object_category == GameObjectCategory.Rat:

            # Player take damage
            if current_time - self.parent.last_damage_time >= self.parent.damage_cooldown:
                self.parent.is_damaged = True
                self.parent.damage(colliding_game_object.attack_damage)
                print("Health: ", self.parent.health)
                self.parent.last_damage_time = current_time

            else:
                self.parent.is_damaged = False

            # Enemy take damage
            player_active_take = self.parent.get_component(SpriteAnimator2D).active_take
            if player_active_take == ActiveTake.PLAYER_ATTACK_X or \
                    player_active_take == ActiveTake.PLAYER_ATTACK_UP or \
                    player_active_take == ActiveTake.PLAYER_ATTACK_DOWN:
                if current_time - colliding_game_object.last_damage_time >= colliding_game_object.damage_cooldown:
                    colliding_game_object.is_damaged = True
                    colliding_game_object.damage(self.parent.attack_damage)
                    colliding_game_object.last_damage_time = current_time
                    print("Enemy health: ", colliding_game_object.health)
                else:
                    colliding_game_object.is_damaged = False

            if self.parent.health == 0:
                self.parent.health = Constants.Player.DEFAULT_HEALTH
                self.parent.lose_live()

            if colliding_game_object.health == 0:
                print("Enemy dead")
                # TODO: this is a temporary fix for testing purposes
                colliding_game_object.remove_component(SpriteRenderer2D)
                colliding_game_object.remove_component(BoxCollider2D)
                colliding_game_object.remove_component(SpriteAnimator2D)
