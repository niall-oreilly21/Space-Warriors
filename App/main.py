import pygame
from pygame import Vector2

from Engine.GameObjects.GameObject import GameObjectType, GameObjectCategory
from Engine.Time.GameTime import GameTime
from Engine.GameObjects.Player import Player
from Engine.Components.PlayerController import PlayerController
from Engine.Managers.RendererManager import RendererManager
from Engine.Managers.Scene import Scene
from Engine.Managers.SceneManager import SceneManager
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Materials.TextMaterial2D import TextMaterial2D
from Engine.Graphics.Materials.TextureMaterial2D import TextureMaterial2D
from Engine.Other.Transform2D import Transform2D


def update(game_time):
    scene.update(game_time)

# Initialize Pygame
pygame.init()

# Set up the display window
screen_width = 640
screen_height = 480

screen = pygame.display.set_mode((screen_width, screen_height))

# Create a font object
font = pygame.font.Font(None, 36)

text_material = TextMaterial2D(font, "Hello, World!", Vector2(0, 0), (255, 0, 0))
sprite_transform = Transform2D(Vector2(10, 100), Vector2(1, 1), 0)

scene = Scene("New Scene")
player = Player("Player", Transform2D(Vector2(10, 200), Vector2(0, 0), Vector2(0, 0)), GameObjectType.Dynamic, GameObjectCategory.Player)

scene.add(player)

# Load an image and create a TextureMaterial2D object with it
image = pygame.image.load("App/image.png")
print("Image dimensions:", image.get_width(), image.get_height())
material = TextureMaterial2D(image, None, 0, (0, 0), None)

sceneManager = SceneManager()

sceneManager.add("Game", scene)
sceneManager.set_active_scene("Game")
renderManager = RendererManager(screen, sceneManager)

frame_rects = []

rect = pygame.Rect(234, 120, 60, 72)
frame_rects.append(rect)
rect = pygame.Rect(342, 120, 60, 72)
frame_rects.append(rect)

sprite_sheet = pygame.image.load("App/image.png")
animator = SpriteAnimator2D("animator", frame_rects, material, 5)





renderer = SpriteRenderer2D("renderer", material)
player.add_component(renderer)

playerController = PlayerController("Player movement", 0.3, 0.3)
player.add_component(playerController)

player.add_component(animator)


scene.add(player)

game_time = GameTime()


# Fill the screen with a background color
background_color = (0, 0, 0) # white
screen.fill(background_color)
# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game_time.tick()
    #text_material.draw(screen, sprite_transform)
    scene.update(game_time)

    screen.fill(background_color)
    renderManager.draw()
    pygame.display.update()
    game_time.limit_fps(60)

pygame.quit()








