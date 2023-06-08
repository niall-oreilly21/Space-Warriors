from pygame import Vector2

from App.Components.Controllers.EnemyController import EnemyController
from App.Constants.Constants import Constants
from Engine.GameObjects.Character import Character
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.GameObjects.Components.Physics.WaypointFinder import WaypointFinder
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Enums.GameObjectEnums import GameObjectType, GameObjectCategory
from Engine.Other.Enums.RendererLayers import RendererLayers
from Engine.Other.Transform2D import Transform2D


class EntityConstants:


    class Enemy:

        WOLF_ENEMY = "wolf enemy"
        dictionary = {
            WOLF_ENEMY : (SpriteRenderer2D(WOLF_ENEMY + "Renderer", Constants.EnemyWolf.MATERIAL_ENEMY1, RendererLayers.Enemy),
                          SpriteAnimator2D(WOLF_ENEMY, Constants.EnemyWolf.ENEMY_ANIMATOR_INFO, Constants.EnemyWolf.MATERIAL_ENEMY1,ActiveTake.ENEMY_WOLF_MOVE_DOWN, Constants.CHARACTER_MOVE_SPEED)),

        }

        enemy = Character("Enemy", 70, 10, 1, Vector2(0, 0), Transform2D(Vector2(0, 0), 0, Vector2(1.5, 1.5)), GameObjectType.Dynamic, GameObjectCategory.Entity)
        enemy.add_component(BoxCollider2D("Box-1"))
        enemy.add_component(Rigidbody2D("Rigid"))
        enemy.add_component(WaypointFinder("Waypoint finder", [Vector2(2000, 4500), Vector2(2200, 4500), Vector2(2400, 4500),Vector2(2800, 4500)]))

        enemy_1 = enemy.clone()

        print(enemy_1.transform)
        # enemy_1.name = "NAthan"
        # enemy_1.transform.position = Vector2(0,0)
        # enemy_1.initial_position = Vector2(1,1)
        # enemy_1.get_component(WaypointFinder).waypoints = []
        # enemy_1.add_component(dictionary[WOLF_ENEMY][0].clone())
        # enemy_1.add_component(dictionary[WOLF_ENEMY][1].clone())



        # material_enemy = Constants.EnemyRat.MATERIAL_ENEMY1
        # enemy.add_component(SpriteRenderer2D("enemy", material_enemy, 0))
        #DICTIONARY FOR ANIMATORS
        #ANIMATOR_RAT = SpriteAnimator2D("enemy", Constants.EnemyRat.ENEMY_ANIMATOR_INFO, material_enemy,ActiveTake.ENEMY_RAT_MOVE_DOWN, Constants.CHARACTER_MOVE_SPEED)



