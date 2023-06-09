import pygame


class ImageLoader:
    images = {}

    RUINS = "Assets/SpriteSheets/Tilesets/Assets_source.png"
    TREES = "Assets/SpriteSheets/Tilesets/plain_tileset.png"
    ROCKS = "Assets/SpriteSheets/Tilesets/Rocks_source.png"
    BUSHES = "Assets/SpriteSheets/Tilesets/Bushes_source.png"
    TILESETS = "Assets/SpriteSheets/Tilesets/plain_tileset2.png"
    POTION_SPEED = "Assets/UI/PowerUps/potion_speed.png"
    POTION_DEFENSE = "Assets/UI/PowerUps/potion_defense.png"
    POTION_HEAL = "Assets/UI/PowerUps/potion_heal.png"
    POTION_ATTACK = "Assets/UI/PowerUps/potion_attack.png"
    POTION_RANDOM = "Assets/UI/PowerUps/random.png"
    HEALTH_BAR = "Assets/UI/health_bar.png"
    TELEPORTER = "Assets/SpriteSheets/teleporter.png"
    PLAYER_GIRL = "Assets/SpriteSheets/Characters/player_girl.png"
    PLAYER_BOY = "Assets/SpriteSheets/Characters/player_boy.png"
    ENEMY_RAT1 = "Assets/SpriteSheets/Characters/enemy_rat1.png"
    ENEMY_RAT2 = "Assets/SpriteSheets/Characters/enemy_rat2.png"
    ENEMY_RAT3 = "Assets/SpriteSheets/Characters/enemy_rat3.png"
    ENEMY_WOLF1 = "Assets/SpriteSheets/Characters/enemy_wolf1.png"
    ENEMY_WOLF2 = "Assets/SpriteSheets/Characters/enemy_wolf2.png"
    ENEMY_WOLF3 = "Assets/SpriteSheets/Characters/enemy_wolf3.png"
    ENEMY_ALIEN1 = "Assets/SpriteSheets/Characters/enemy_alien1.png"
    ENEMY_ALIEN2 = "Assets/SpriteSheets/Characters/enemy_alien2.png"
    ENEMY_ALIEN3 = "Assets/SpriteSheets/Characters/enemy_alien3.png"
    PET_DOG = "Assets/SpriteSheets/Characters/pet_dog.png"
    MAIN_MENU_BACKGROUND = "Assets/UI/Menu/main_menu.png"
    PLAIN_MENU_BACKGROUND = "Assets/UI/Menu/plain_menu.png"
    STARS = "Assets/UI/stars.png"
    MENU_BUTTON = "Assets/UI/Menu/menu_button.png"
    EARTH = "Assets/UI/Menu/earth.png"
    MARS = "Assets/UI/Menu/mars.png"
    SATURN = "Assets/UI/Menu/saturn.png"
    SPOTLIGHT = "Assets/UI/circle.png"

    def load_image(self, path):
        if path in self.images:
            return
        else:
            image = pygame.image.load(path).convert_alpha()
            self.images[path] = image

    def get_image(self, path):
        return self.images[path]
