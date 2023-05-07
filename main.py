import pygame
from pygame import Vector2

from Material2D import Material
from SpriteRenderer2D import SpriteRenderer2D
from Component import Component
from PlayerController import PlayerController
from Player import Player
from Renderer2D import Renderer2D
from Sprite import Sprite
from TextMaterial2D import TextMaterial2D
from TextureMaterial2D import TextureMaterial2D
from Transform2D import Transform2D
from GameTime import GameTime
from Scene import Scene
from GameObject import GameObjectCategory
from GameObject import GameObjectType
from SpriteAnimator2D import SpriteAnimator2D

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
player.add_component(PlayerController("Player movement", 0.3, 0.3))
scene.add(player)

# Load an image and create a TextureMaterial2D object with it
image = pygame.image.load("image.png")
print("Image dimensions:", image.get_width(), image.get_height())
material = TextureMaterial2D(image, None, 0, (0, 0), None)


frame_rects = []

rect = pygame.Rect(234, 120, 60, 72)
frame_rects.append(rect)
# rect = pygame.Rect(342, 120, 60, 72)
frame_rects.append(rect)

sprite_sheet = pygame.image.load("image.png")
animator = SpriteAnimator2D("animator", frame_rects, material, 7)


# Draw the texture onto the Surface
#sprite_animator = Sprite2DAnimator("animator", frame_rects, material, fps=5)
player.add_component(animator)
renderer = SpriteRenderer2D("renderer", material)
#player.add_component(sprite_animator)
player.add_component(renderer)


scene.add(player)

game_time = GameTime()

# Create a surface to draw on
circle_radius = 50
circle_color = (0, 0, 255) # blue
circle_surface = pygame.Surface((circle_radius * 2, circle_radius * 2), pygame.SRCALPHA)

# Draw the circle on the surface
#pygame.draw.circle(circle_surface, circle_color, (circle_radius, circle_radius), circle_radius)
# Fill the screen with a background color
background_color = (0, 0, 0) # white
screen.fill(background_color)
# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the circle on the center of the screen
    #screen.blit(circle_surface, (screen_width // 2 - circle_radius, screen_height // 2 - circle_radius))
    # Draw the renderer onto the screen
    #renderer.draw(screen)
    #Update the display
    text_material.draw(screen, sprite_transform)
    scene.update(game_time)
    renderer.draw(screen)
    pygame.display.update()

    screen.fill(background_color)

pygame.quit()








