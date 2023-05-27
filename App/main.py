import math
import os
import pygame
from pygame import Vector2, Rect

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

cameraGameObject = GameObject("MainCamera", Transform2D(Vector2(0, 300), Vector2(0, 0), Vector2(0, 0)), GameObjectType.Dynamic, GameObjectCategory.Player)
camera = Camera("MainCamera", 1000, 500)
cameraGameObject.add_component(camera)
managers = []
sceneManager = SceneManager()

cameraManager = CameraManager(screen, sceneManager)
cameraManager.add(cameraGameObject)

cameraManager.set_active_camera("MainCamera")

# Create a font object
font = pygame.font.Font(None, 80)
font_name = None


text_material = TextMaterial2D(font, font_name, "Hello, World!", Vector2(150,40), (255, 0, 0))
sprite_transform = Transform2D(Vector2(10, 100), 0, Vector2(1, 1))

scene = Scene("New Scene")
player = GameObject("Player", Transform2D(Vector2(0, 300), 0, Vector2(1, 1)), GameObjectType.Dynamic, GameObjectCategory.Player)
player.add_component(Rigidbody2D("Rigid"))
player.add_component(BoxCollider2D("Box"))
#player.add_component(Rigidbody2D("Body"))

enemy = GameObject("Enemy", Transform2D(Vector2(100, 100), 0, Vector2(4, 4)), GameObjectType.Dynamic, GameObjectCategory.Player)
enemy.add_component(BoxCollider2D("Box-1"))


text = GameObject("Text", Transform2D(Vector2(0, 0),0, Vector2(1, 1)), GameObjectType.Dynamic, GameObjectCategory.Player)

image = pygame.image.load("menu_button.png")
texture_material = TextureMaterial2D(image, None, 0, Vector2(0, 0), None)
text.add_component(Renderer2D("Renderer-2", texture_material, 1))
text.add_component(Renderer2D("Renderer-1", text_material, 2))

text.add_component(BoxCollider2D("Box-2"))

scene.add(player)
scene.add(enemy)
scene.add(text)


# Load an image and create a TextureMaterial2D object with it
image = pygame.image.load("image.png")
material = TextureMaterial2D(image, None, 0, Vector2(0, 0), None)

material2 = TextureMaterial2D(image, (255,255,0), 0, Vector2(0, 0), None)

enemy.add_component(SpriteRenderer2D("renderer-enemy", material2, 3))


sceneManager.add("Game", scene)
sceneManager.set_active_scene("Game")
renderManager = RendererManager(screen, sceneManager, cameraManager)

frame_rects = []

rect = pygame.Rect(234, 120, 60, 72)
frame_rects.append(rect)
rect = pygame.Rect(342, 120, 60, 72)
frame_rects.append(rect)

frame_rects2 = []

rect = pygame.Rect(18, 6, 60, 90)
frame_rects2.append(rect)
rect = pygame.Rect(126, 6, 60, 90)
frame_rects2.append(rect)

frame_rects3 = [Rect(6, 114, 84, 84)]

animator_info = [Take(ActiveTake.PLAYER_RUNNING, frame_rects), Take(ActiveTake.PLAYER_WALKING, frame_rects2), Take(ActiveTake.COOK, frame_rects3)]

animator = SpriteAnimator2D("animator", animator_info, material, ActiveTake.COOK, 0.8)
renderer = SpriteRenderer2D("renderer", material, 4)
player.add_component(renderer)

playerController = PlayerController("Player movement", 0.3, 0.3)
player.add_component(playerController)

animator1 = SpriteAnimator2D("animator-enemy", animator_info, material2, ActiveTake.COOK, 5)
enemy.add_component(animator1)

player.add_component(animator)

managers.append(cameraManager)
managers.append(sceneManager)


game_time = GameTime()
cameraGameObject.add_component(ThirdPersonController("Third Person Controller", player))

for manager in managers:
    manager.start()
# Fill the screen with a background color
background_color = (0, 0, 0) # white
if screen is  not None:
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

    player.get_component(BoxCollider2D).draw(screen , cameraManager)
    enemy.get_component(BoxCollider2D).draw(screen, cameraManager)
    text.get_component(BoxCollider2D).draw(screen, cameraManager)

    renderManager.draw(game_time)


    pygame.display.update()
    game_time.limit_fps(60)

pygame.quit()








