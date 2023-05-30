import time

from App.Components.Colliders.AttackBoxCollider2D import AttackBoxCollider2D
from App.Components.PlayerController import PlayerController
from App.Constants.Constants import Constants
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Collider2D import Collider2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Enums.GameObjectEnums import GameObjectCategory
from Engine.Other.Interfaces.IDamageable import IDamageable


class PlayerAttackCollider(Collider2D):

    def __init__(self, name):
        super().__init__(name)

    def handle_response(self, parent_game_object):
        current_time = time.time()
        if parent_game_object.game_object_category == GameObjectCategory.Alien or \
                parent_game_object.game_object_category == GameObjectCategory.Wolf or \
                parent_game_object.game_object_category == GameObjectCategory.Rat:
            # player and enemy collide
            # print("cur time ", current_time)
            # print("last damage time", self.parent.last_damage_time)

            if current_time - self.parent.last_damage_time >= self.parent.damage_cooldown:
                # print(self.parent.damage_cooldown)
                self.parent.is_damaged = True
                self.parent.damage(parent_game_object.attack_damage)
                print("Health: ", self.parent.health)
                self.parent.last_damage_time = current_time

            else:
                self.parent.is_damaged = False
            # self = player
            # parent_game_object = enemy

            player_active_take = self.parent.get_component(SpriteAnimator2D).active_take
            if player_active_take == ActiveTake.PLAYER_ATTACK_X or \
                    player_active_take == ActiveTake.PLAYER_ATTACK_UP or \
                    player_active_take == ActiveTake.PLAYER_ATTACK_DOWN:
                if current_time - parent_game_object.last_damage_time >= parent_game_object.damage_cooldown:
                    parent_game_object.is_damaged = True
                    parent_game_object.damage(self.parent.attack_damage)
                    parent_game_object.last_damage_time = current_time
                    print("Enemy health: ", parent_game_object.health)
                else:
                    parent_game_object.is_damaged = False

            if self.parent.health == 0:
                self.parent.health = Constants.Player.DEFAULT_HEALTH
                self.parent.lose_live()

            if parent_game_object.health == 0:
                print("Enemy dead")
                parent_game_object.remove_component(SpriteRenderer2D)
                parent_game_object.remove_component(SpriteAnimator2D)