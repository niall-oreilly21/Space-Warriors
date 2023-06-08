from pygame import Vector2

from App.Components.Controllers.EnemyController import EnemyController
from App.Constants.Application import Application
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
        RAT_ENEMY = "rat enemy"
        ALIEN_ENEMY = "alien enemy"
        dictionary = {
            RAT_ENEMY : (SpriteRenderer2D(RAT_ENEMY + "Renderer", Constants.EnemyRat.MATERIAL_ENEMY1, RendererLayers.Enemy),
                         SpriteAnimator2D(RAT_ENEMY, Constants.EnemyRat.ENEMY_ANIMATOR_INFO, Constants.EnemyRat.MATERIAL_ENEMY1,ActiveTake.ENEMY_RAT_MOVE_DOWN, Constants.CHARACTER_ANIMATOR_MOVE_SPEED)),
            WOLF_ENEMY : (SpriteRenderer2D(WOLF_ENEMY + "Renderer", Constants.EnemyWolf.MATERIAL_ENEMY1, RendererLayers.Enemy),
                          SpriteAnimator2D(WOLF_ENEMY, Constants.EnemyWolf.ENEMY_ANIMATOR_INFO, Constants.EnemyWolf.MATERIAL_ENEMY1,ActiveTake.ENEMY_WOLF_MOVE_DOWN, Constants.CHARACTER_ANIMATOR_MOVE_SPEED)),
            ALIEN_ENEMY: (SpriteRenderer2D(ALIEN_ENEMY + "Renderer", Constants.EnemyAlien.MATERIAL_ENEMY1, RendererLayers.Enemy),
                          SpriteAnimator2D(ALIEN_ENEMY, Constants.EnemyAlien.ENEMY_ANIMATOR_INFO, Constants.EnemyAlien.MATERIAL_ENEMY1,
                             ActiveTake.ENEMY_ALIEN_MOVE_DOWN, Constants.CHARACTER_ANIMATOR_MOVE_SPEED)),

        }

        enemy = Character("Enemy", 70, 10, 1, Vector2(0, 0), Transform2D(Vector2(0, 0), 0, Vector2(1.5, 1.5)), GameObjectType.Dynamic, GameObjectCategory.Entity)
        enemy.add_component(BoxCollider2D("Box-1"))
        enemy.add_component(Rigidbody2D("Rigid"))
        enemy.add_component(WaypointFinder("Waypoint finder", [Vector2(2000, 4500), Vector2(2200, 4500), Vector2(2400, 4500),Vector2(2800, 4500)]))


        wolf = enemy.clone()

        wolf.name = WOLF_ENEMY
        wolf.transform.position = Vector2(0, 0)
        wolf.initial_position = Vector2(4000, 3500)
        wolf.get_component(WaypointFinder).waypoints = [Vector2(4000,3500), Vector2(4800,3500), Vector2(4800,2900), Vector2(3700,2900)]
        wolf.add_component(dictionary[WOLF_ENEMY][0].clone())
        wolf.add_component(dictionary[WOLF_ENEMY][1].clone())
        print(Application.Player)
        wolf.add_component(EnemyController("Enemy movement", Application.Player, Constants.EnemyWolf.MOVE_SPEED, 200))

        alien = enemy.clone()

        alien.name = ALIEN_ENEMY
        alien.transform.position = Vector2(2900, 4900)
        alien.initial_position = Vector2(2900, 4900)
        alien.get_component(WaypointFinder).waypoints = []
        alien.add_component(dictionary[ALIEN_ENEMY][0].clone())
        alien.add_component(dictionary[ALIEN_ENEMY][1].clone())

        rat = enemy.clone()

        rat.name = RAT_ENEMY
        rat.transform.position = Vector2(0, 0)
        rat.initial_position = Vector2(1, 1)
        rat.get_component(WaypointFinder).waypoints = []
        rat.add_component(dictionary[RAT_ENEMY][0].clone())
        rat.add_component(dictionary[RAT_ENEMY][1].clone())

