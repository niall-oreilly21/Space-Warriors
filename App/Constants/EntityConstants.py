import pygame
from pygame import Vector2

from App.Components.Controllers.EnemyController import EnemyController
from App.Components.Controllers.EnemyHealthBarController import EnemyHealthBarController
from App.Constants.Application import Application
from App.Constants.GameConstants import GameConstants
from Engine.GameObjects.Character import Character
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.GameObjects.Components.Physics.WaypointFinder import WaypointFinder
from Engine.GameObjects.GameObject import GameObject
from Engine.Graphics.Materials.RectMaterial2D import RectMaterial2D
from Engine.Graphics.Materials.TextureMaterial2D import TextureMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Other.Enums.GameObjectEnums import GameObjectType, GameObjectCategory
from Engine.Other.Enums.RendererLayers import RendererLayers
from Engine.Other.Transform2D import Transform2D


class EntityConstants:
    class Player:
        PLAYER_INITIAL_POSITION_EARTH = Vector2(2900, 4900)
        PLAYER_INITIAL_POSITION_MARS = Vector2(3640, 4700)
        PLAYER_INITIAL_POSITION_SATURN = Vector2(2550, 3500)
        PLAYER_INITIAL_POSITION_HOUSE = Vector2(459, 418)
        PLAYER = Character("Player", GameConstants.Player.DEFAULT_HEALTH, GameConstants.Player.DEFAULT_ATTACK_DAMAGE,
                           GameConstants.Player.DAMAGE_COOLDOWN, Vector2(2900, 4900),
                           Transform2D(Vector2(2900, 4900), 0, Vector2(1.2, 1.2)),
                           GameObjectType.Dynamic, GameObjectCategory.Player)

    class Pet:
        PET = GameObject("PetDog", Transform2D(Vector2(7210, 5500), 0, Vector2(1.2, 1.2)), GameObjectType.Dynamic,GameObjectCategory.Pet)

    class Enemy:
        WOLF_ENEMY_NAME = "wolf enemy"
        RAT_ENEMY_NAME = "rat enemy"
        ALIEN_ENEMY_NAME = "alien enemy"
        enemy_sprites = {
            RAT_ENEMY_NAME: (
                SpriteRenderer2D(RAT_ENEMY_NAME + "Renderer", GameConstants.EnemyRat.MATERIAL_ENEMY1, RendererLayers.Enemy),
                SpriteAnimator2D(RAT_ENEMY_NAME, GameConstants.EnemyRat.ENEMY_ANIMATOR_INFO,
                                 GameConstants.EnemyRat.MATERIAL_ENEMY1,
                                 ActiveTake.ENEMY_RAT_MOVE_DOWN, GameConstants.CHARACTER_ANIMATOR_MOVE_SPEED)),
            WOLF_ENEMY_NAME: (
                SpriteRenderer2D(WOLF_ENEMY_NAME + "Renderer", GameConstants.EnemyWolf.MATERIAL_ENEMY1,
                                 RendererLayers.Enemy),
                SpriteAnimator2D(WOLF_ENEMY_NAME, GameConstants.EnemyWolf.ENEMY_ANIMATOR_INFO,
                                 GameConstants.EnemyWolf.MATERIAL_ENEMY1, ActiveTake.ENEMY_WOLF_MOVE_DOWN,
                                 GameConstants.CHARACTER_ANIMATOR_MOVE_SPEED)),
            ALIEN_ENEMY_NAME: (
                SpriteRenderer2D(ALIEN_ENEMY_NAME + "Renderer", GameConstants.EnemyAlien.MATERIAL_ENEMY1,
                                 RendererLayers.Enemy),
                SpriteAnimator2D(ALIEN_ENEMY_NAME, GameConstants.EnemyAlien.ENEMY_ANIMATOR_INFO,
                                 GameConstants.EnemyAlien.MATERIAL_ENEMY1,
                                 ActiveTake.ENEMY_ALIEN_MOVE_DOWN, GameConstants.CHARACTER_ANIMATOR_MOVE_SPEED)),

        }

        enemy = Character("Enemy", GameConstants.EnemyRat.HEALTH, GameConstants.EnemyRat.ATTACK_DAMAGE, 1, Vector2(0, 0),
                          Transform2D(Vector2(0, 0), 0, Vector2(1.5, 1.5)),
                          GameObjectType.Dynamic, GameObjectCategory.Rat)
        enemy.add_component(BoxCollider2D("Box-1"))
        enemy.add_component(Rigidbody2D("Rigid"))
        enemy.add_component(WaypointFinder("Waypoint finder",
                                           [Vector2(2000, 4500), Vector2(2200, 4500), Vector2(2400, 4500),
                                            Vector2(2800, 4500)]))

        RAT_ENEMY = enemy.clone()

        RAT_ENEMY.name = RAT_ENEMY_NAME
        RAT_ENEMY.transform.position = Vector2(0, 0)
        RAT_ENEMY.initial_position = Vector2(4000, 3500)
        RAT_ENEMY.get_component(WaypointFinder).waypoints = [Vector2(4000, 3500), Vector2(4800, 3500),
                                                             Vector2(4800, 3200), Vector2(3700, 3200)]
        RAT_ENEMY.add_component(enemy_sprites[RAT_ENEMY_NAME][0].clone())
        RAT_ENEMY.add_component(enemy_sprites[RAT_ENEMY_NAME][1].clone())

        WOLF_ENEMY = enemy.clone()

        WOLF_ENEMY.name = WOLF_ENEMY_NAME
        WOLF_ENEMY.game_object_category = GameObjectCategory.Wolf
        WOLF_ENEMY.transform.position = Vector2(0, 0)
        WOLF_ENEMY.initial_position = Vector2(2470, 4065)
        WOLF_ENEMY.get_component(WaypointFinder).waypoints = [Vector2(2470, 4065), Vector2(2900, 3730),
                                                              Vector2(2540, 3500)]
        WOLF_ENEMY.add_component(enemy_sprites[WOLF_ENEMY_NAME][0].clone())
        WOLF_ENEMY.add_component(enemy_sprites[WOLF_ENEMY_NAME][1].clone())
        WOLF_ENEMY.health = GameConstants.EnemyWolf.HEALTH
        WOLF_ENEMY.attack_damage = GameConstants.EnemyWolf.ATTACK_DAMAGE

        ALIEN_ENEMY = enemy.clone()

        ALIEN_ENEMY.name = ALIEN_ENEMY_NAME
        ALIEN_ENEMY.game_object_category = GameObjectCategory.Alien
        ALIEN_ENEMY.transform.position = Vector2(2900, 4900)
        ALIEN_ENEMY.initial_position = Vector2(4110, 4366)
        ALIEN_ENEMY.get_component(WaypointFinder).waypoints = [Vector2(4110, 3666), Vector2(3185, 4136),
                                                               Vector2(4110, 3050), Vector2(3580, 3050)]
        ALIEN_ENEMY.add_component(enemy_sprites[ALIEN_ENEMY_NAME][0].clone())
        ALIEN_ENEMY.add_component(enemy_sprites[ALIEN_ENEMY_NAME][1].clone())
        ALIEN_ENEMY.health = GameConstants.EnemyAlien.HEALTH
        ALIEN_ENEMY.attack_damage = GameConstants.EnemyAlien.ATTACK_DAMAGE

        HOUSE_RAT_ENEMY_NAME = "HouseRat"

        ENEMY_WAYPOINTS = {
            HOUSE_RAT_ENEMY_NAME: [
                [Vector2(100, 0), Vector2(400, 0)],
                [Vector2(840, 0), Vector2(840, 200)]
            ],
            RAT_ENEMY_NAME: [
                [Vector2(4000, 3000), Vector2(2600, 4000), Vector2(4500, 3100), Vector2(3800, 3100)],
                [Vector2(4200, 3200), Vector2(4500, 3200), Vector2(4500, 3200), Vector2(3800, 3200)],
                [Vector2(4700, 2300), Vector2(5300, 2300), Vector2(5300, 1800), Vector2(4700, 1800)],
                [Vector2(4800, 2400), Vector2(5200, 2400), Vector2(5200, 1900), Vector2(4800, 1900)],
                [Vector2(3000, 4000), Vector2(3500, 4200), Vector2(3500, 4100), Vector2(2800, 4200)],
                [Vector2(2736, 2855), Vector2(3120, 2855)],
                [Vector2(4700, 5300), Vector2(5300, 5300), Vector2(5300, 4800), Vector2(4700, 4800)],
                [Vector2(4800, 2400), Vector2(5200, 2400), Vector2(5200, 1900), Vector2(4800, 1900)],
                [Vector2(2000, 2000), Vector2(2200, 2100), Vector2(2400, 2000), Vector2(2600, 2100)],
                [Vector2(2000, 4200), Vector2(2200, 4200), Vector2(2400, 4200), Vector2(2600, 4200)],
                [Vector2(5500, 5500), Vector2(5900, 5700), Vector2(6000, 5500), Vector2(5500, 1800)],
                [Vector2(5800, 2800), Vector2(5000, 5500)],
                [Vector2(3071, 2602), Vector2(2752, 2602)],
                [Vector2(4052, 1328), Vector2(3700, 1328)],
                [Vector2(4738, 3780), Vector2(3950, 3780)]
            ],
            WOLF_ENEMY_NAME: [
                [Vector2(2550, 3500), Vector2(3000, 3000), Vector2(2800, 3100), Vector2(3000, 2800)],
                [Vector2(2690, 4552), Vector2(2392, 4051), Vector2(2660, 3844), Vector2(2600, 3000)],
                [Vector2(1637, 3372), Vector2(1885, 3195), Vector2(1583, 2845), Vector2(1976, 2405)],
                [Vector2(4700, 1467), Vector2(5014, 1663), Vector2(5668, 1834), Vector2(6875, 1366)],
                [Vector2(5546, 2034), Vector2(4706, 2034), Vector2(5252, 2193), Vector2(5423, 2518)],
                [Vector2(3770, 2004), Vector2(3770, 1700), Vector2(4174, 1700), Vector2(4174, 2034)],
                [Vector2(1848, 1231), Vector2(3061, 1231)],
                [Vector2(1769, 5521), Vector2(3311, 5916)],
                [Vector2(5112, 1943), Vector2(5112, 2817)],
                [Vector2(3962, 3389), Vector2(3962, 4000)],
            ],
            ALIEN_ENEMY_NAME: [
                [Vector2(2355, 1841), Vector2(2500, 1841)],#Boss
                [Vector2(2355, 1841), Vector2(2500, 1841)],
                [Vector2(1970, 5580), Vector2(2272, 5368), Vector2(2575, 5527), Vector2(1981, 5188)],
                [Vector2(5297, 4770), Vector2(4827, 4770), Vector2(4911, 4913), Vector2(4547, 4913)],
                [Vector2(4907, 1456), Vector2(4907, 1964), Vector2(6661, 1964)],
                [Vector2(3619, 3913), Vector2(2870, 3913)]
            ],
        }
