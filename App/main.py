import math
import os
import pygame
from pygame import Vector2, Rect

from App.Components.EnemyController import EnemyController
from App.Constants.Constants import Constants
from Engine.Other.Enums.GameObjectEnums import GameObjectEnemyType
from Engine.GameObjects.Components.Cameras.Camera import Camera
from Engine.GameObjects.Components.Cameras.ThirdPersonController import ThirdPersonController
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.Components.Cameras.Camera import Camera
from Engine.GameObjects.GameObject import GameObjectType, GameObjectCategory, GameObject
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Sprites.Take import Take
from Engine.Managers.CameraManager import CameraManager
from Engine.Other.Enums.ActiveTake import ActiveTake
from Engine.Time.GameTime import GameTime
from App.Components.PlayerController import PlayerController
from Engine.Managers.RendererManager import RendererManager
from Engine.Managers.Scene import Scene
from Engine.Managers.SceneManager import SceneManager
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Materials.TextMaterial2D import TextMaterial2D
from Engine.Graphics.Materials.TextureMaterial2D import TextureMaterial2D
from Engine.GameObjects.Components.Physics.Rigidbody2D import Rigidbody2D
from Engine.Other.Transform2D import Transform2D


def resolve_collision(collider1, collider2):
    # Example collision response logic
    # Modify the positions, velocities, or other properties of the colliding objects

    # Example separation
    collider1_transform = collider1.parent.get_component(Transform2D)
    collider2_transform = collider2.parent.get_component(Transform2D)
    collider1_position = collider1.parent.get_component(Transform2D)
    collider2_position = collider2_transform.position

    # Calculate the separation vector
    separation_vector = collider1.bounds.clip(collider2.bounds).size

    # Separate the colliders
    collider1_position -= separation_vector / 2
    collider2_position += separation_vector / 2


def update(game_time):
    scene.update(game_time)


# Initialize Pygame
pygame.init()

# Set up the display window
screen_width = 1
screen_height = 1

# # Create the display window
screen_info = pygame.display.Info()
screen_resolution = Vector2(screen_info.current_w, screen_info.current_h)

# Set the environment variable to center the window
os.environ['SDL_VIDEO_CENTERED'] = '1'

screen = pygame.display.set_mode((400, 400))

cameraGameObject = GameObject("MainCamera", Transform2D(Vector2(0, 300), Vector2(0, 0), Vector2(0, 0)),
                              GameObjectType.Dynamic, GameObjectCategory.Player)
camera = Camera("MainCamera", 1000, 500)
cameraGameObject.add_component(camera)
managers = []
sceneManager = SceneManager()

cameraManager = CameraManager(screen, sceneManager)
cameraManager.add(cameraGameObject)

cameraManager.set_active_camera("MainCamera")

# Create a font object
font_path = "Assets/Fonts/Starjedi.ttf"
font = pygame.font.Font(font_path, 80)
font_name = font_path

text_material = TextMaterial2D(font, font_name, "Hello, World!", Vector2(150, 40), (255, 0, 0))
sprite_transform = Transform2D(Vector2(10, 100), 0, Vector2(1, 1))

scene = Scene("New Scene")
player = GameObject("Player", Transform2D(Vector2(300, 300), 0, Vector2(1, 1)), GameObjectType.Dynamic,
                    GameObjectCategory.Player)
player.add_component(Rigidbody2D("Rigid"))
player.add_component(BoxCollider2D("Box"))
material_player = Constants.Player.MATERIAL_GIRL
player.add_component(SpriteRenderer2D("player", material_player, 1))
player.add_component(SpriteAnimator2D("player", Constants.Player.PLAYER_ANIMATOR_INFO, material_player,
                                      ActiveTake.PLAYER_IDLE_DOWN, Constants.CHARACTER_MOVE_SPEED))
playerController = PlayerController("Player movement", 0.3, 0.3)
player.add_component(playerController)

enemy = GameObject("Enemy", Transform2D(Vector2(5000, 5000), 0, Vector2(1.5, 1.5)), GameObjectType.Dynamic,
                   GameObjectCategory.Player)
enemy.add_component(BoxCollider2D("Box-1"))
# enemy.add_component(Rigidbody2D("Rigid"))
material_enemy = Constants.EnemyRat.MATERIAL_ENEMY1
enemy.add_component(SpriteRenderer2D("enemy", material_enemy, 1))
enemy.add_component(SpriteAnimator2D("enemy", Constants.EnemyRat.ENEMY_ANIMATOR_INFO, material_enemy,
                                     ActiveTake.ENEMY_RAT_MOVE_DOWN, Constants.CHARACTER_MOVE_SPEED))
enemy_controller = EnemyController("Enemy movement", player, Constants.EnemyRat.MOVE_SPEED, GameObjectEnemyType.Rat)
enemy.add_component(enemy_controller)

enemy2 = GameObject("Enemy2", Transform2D(Vector2(-1000, -1000), 0, Vector2(1.5, 1.5)), GameObjectType.Dynamic,
                    GameObjectCategory.Player)
enemy2.add_component(BoxCollider2D("Box-3"))
# enemy.add_component(Rigidbody2D("Rigid"))
material_enemy = Constants.EnemyWolf.MATERIAL_ENEMY1
enemy2.add_component(SpriteRenderer2D("enemy2", material_enemy, 1))
enemy2.add_component(SpriteAnimator2D("enemy2", Constants.EnemyWolf.ENEMY_ANIMATOR_INFO, material_enemy,
                                      ActiveTake.ENEMY_WOLF_MOVE_DOWN, Constants.CHARACTER_MOVE_SPEED))
enemy_controller2 = EnemyController("Enemy movement 2", player, Constants.EnemyWolf.MOVE_SPEED, GameObjectEnemyType.Wolf)
enemy2.add_component(enemy_controller2)

enemy3 = GameObject("Enemy3", Transform2D(Vector2(1000, -1000), 0, Vector2(1.5, 1.5)), GameObjectType.Dynamic,
                    GameObjectCategory.Player)
enemy3.add_component(BoxCollider2D("Box-4"))
# enemy.add_component(Rigidbody2D("Rigid"))
material_enemy = Constants.EnemyAlien.MATERIAL_ENEMY1
enemy3.add_component(SpriteRenderer2D("enemy3", material_enemy, 1))
enemy3.add_component(SpriteAnimator2D("enemy3", Constants.EnemyAlien.ENEMY_ANIMATOR_INFO, material_enemy,
                                      ActiveTake.ENEMY_ALIEN_MOVE_DOWN, Constants.CHARACTER_MOVE_SPEED))
enemy_controller3 = EnemyController("Enemy movement 3", player, Constants.EnemyAlien.MOVE_SPEED, GameObjectEnemyType.Alien)
enemy3.add_component(enemy_controller3)

enemy4 = GameObject("Enemy4", Transform2D(Vector2(750, 0), 0, Vector2(1.5, 1.5)), GameObjectType.Dynamic,
                    GameObjectCategory.Player)
enemy4.add_component(BoxCollider2D("Box-5"))
# enemy.add_component(Rigidbody2D("Rigid"))
material_enemy = Constants.EnemyAlien.MATERIAL_ENEMY3
enemy4.add_component(SpriteRenderer2D("enemy4", material_enemy, 1))
enemy4.add_component(SpriteAnimator2D("enemy4", Constants.EnemyAlien.ENEMY_ANIMATOR_INFO, material_enemy,
                                      ActiveTake.ENEMY_ALIEN_MOVE_DOWN, Constants.CHARACTER_MOVE_SPEED))
enemy_controller4 = EnemyController("Enemy movement 4", player, Constants.EnemyAlien.MOVE_SPEED, GameObjectEnemyType.Alien)
enemy4.add_component(enemy_controller4)

text = GameObject("Text", Transform2D(Vector2(0, 0), 0, Vector2(1, 1)), GameObjectType.Dynamic,
                  GameObjectCategory.Player)

image = pygame.image.load("menu_button.png")
texture_material = TextureMaterial2D(image, None, 0, Vector2(0, 0), None)
text.add_component(Renderer2D("Renderer-2", texture_material, 1))
text.add_component(Renderer2D("Renderer-1", text_material, 2))
text.add_component(BoxCollider2D("Box-2"))

scene.add(player)
scene.add(enemy)
scene.add(enemy2)
scene.add(enemy3)
scene.add(enemy4)
scene.add(text)

sceneManager.add("Game", scene)
sceneManager.set_active_scene("Game")
renderManager = RendererManager(screen, sceneManager, cameraManager)

managers.append(cameraManager)
managers.append(sceneManager)

game_time = GameTime()
cameraGameObject.add_component(ThirdPersonController("Third Person Controller", player))
# sceneManager.set_active_scene("Main Menu")
for manager in managers:
    manager.start()
# Fill the screen with a background color
background_color = (0, 0, 0)  # white
if screen is not None:
    screen.fill(background_color)
# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if player.get_component(BoxCollider2D).collides_with(enemy.get_component(BoxCollider2D)):
        player_collider = player.get_component(BoxCollider2D)
        enemy_collider = enemy.get_component(BoxCollider2D)
        print("collide")

        player_velocity = player.get_component(Rigidbody2D).velocity

        offset = 0

        # Adjust player's position to prevent passing through enemy horizontally
        if player_collider.bounds.right > enemy_collider.bounds.left and player_collider.bounds.left < enemy_collider.bounds.left:
            player.transform.position.x = enemy_collider.bounds.left - player_collider.bounds.width
        elif player_collider.bounds.left < enemy_collider.bounds.right and player_collider.bounds.right > enemy_collider.bounds.right:
            player.transform.position.x = enemy_collider.bounds.right

        # Adjust player's position to prevent passing through enemy vertically
        if player_collider.bounds.bottom > enemy_collider.bounds.top and player_collider.bounds.top < enemy_collider.bounds.top:
            player.transform.position.y = enemy_collider.bounds.top - player_collider.bounds.height
        elif player_collider.bounds.top < enemy_collider.bounds.bottom and player_collider.bounds.bottom > enemy_collider.bounds.bottom:
            player.transform.position.y = enemy_collider.bounds.bottom

        # elif self.velocity[0] < 0:  # Moving left
        #     self.rect.left = obj.rect.right
        # if self.velocity[1] > 0:  # Moving down
        #     self.rect.bottom = obj.rect.top
        # elif self.velocity[1] < 0:  # Moving up
        #     self.rect.top = obj.rect.bottom

        # Calculate the overlap depth
        # overlap_x = (player_collider.right - static_object_collider.left) if player.velocity.x > 0 else (
        #             static_object_collider.right - player_collider.left)
        # overlap_y = (player_collider.bottom - static_object_collider.top) if player.velocity.y > 0 else (
        #             static_object_collider.bottom - player_collider.top)
        #
        # if overlap_x > 0 and overlap_y > 0:
        #     # Determine the axis of least penetration
        #     if overlap_x < overlap_y:
        #         # Resolve collision horizontally
        #         if player.velocity.x > 0:
        #             player.transform.position.x = static_object_collider.left - player_collider.width
        #         else:
        #             player.transform.position.x = static_object_collider.right
        #     else:
        #         # Resolve collision vertically
        #         if player.velocity.y > 0:
        #             player.transform.position.y = static_object_collider.top - player_collider.height
        #         else:
        #             player.transform.position.y = static_object_collider.bottom

    game_time.tick()

    for manager in managers:
        manager.update(game_time)

    if screen is not None:
        screen.fill(background_color)

    player.get_component(BoxCollider2D).draw(screen, cameraManager)
    enemy.get_component(BoxCollider2D).draw(screen, cameraManager)
    text.get_component(BoxCollider2D).draw(screen, cameraManager)

    renderManager.draw(game_time)

    pygame.display.update()
    game_time.limit_fps(60)

pygame.quit()
