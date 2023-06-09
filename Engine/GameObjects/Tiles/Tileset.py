import pygame
from pygame import Vector2, Rect

from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.Graphics.Materials.TextureMaterial2D import TextureMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Renderers.SpriteRenderer2D import SpriteRenderer2D
from Engine.Graphics.Sprites.Sprite import Sprite
from Engine.Other.Enums.RendererLayers import RendererLayers


class Tileset:
    def __init__(self, sprite_sheet_path, tile_width, tile_height):
        self.tiles = []
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert()
        self.__tile_width = tile_width
        self.__tile_height = tile_height
        self.__surfaces = {}


    def add_tile(self, tile):
        self.tiles.append(tile)


    def __set_scaled_surfaces(self, tile_id, source_rect):

        if tile_id in self.__surfaces:
            return self.__surfaces[tile_id]

        texture_surface = pygame.Surface(source_rect.size, pygame.SRCALPHA)
        texture_surface.blit(self.sprite_sheet, (0, 0), source_rect)

        self.__surfaces[tile_id] = texture_surface
        return self.__surfaces[tile_id]


    def get_tile(self, tile_id):
        for tile in self.tiles:
            if tile.tile_id == tile_id:
                return tile
        return None

    def create_map(self, map_data):
        tile_dict = {tile.tile_id: tile.clone() for tile in self.tiles}
        map_width = len(map_data[0])
        map_height = len(map_data)

        map_tiles = []
        for y in range(map_height):
            row = []
            for x in range(map_width):
                current_tile_attributes = map_data[y][x]

                current_tile = tile_dict.get(current_tile_attributes.tile_id).clone()

                if current_tile is not None:
                    current_tile.transform.position = Vector2(x * self.__tile_width, y * self.__tile_height)

                    ## Set sprite image for the cloned tile
                    tile_position = current_tile.position_on_sprite_sheet

                    tile_material = TextureMaterial2D(self.sprite_sheet, None, Vector2(0, 0), None, self.__set_scaled_surfaces(current_tile.tile_id, Rect(tile_position.x, tile_position.y ,self.__tile_width, self.__tile_height)))

                    current_tile.add_component(SpriteRenderer2D("tile", tile_material, RendererLayers.Background,
                                                                Sprite(self.sprite_sheet, Rect(tile_position.x, tile_position.y ,self.__tile_width, self.__tile_height),
                                                                       current_tile_attributes.color, current_tile_attributes.alpha)))
                    if current_tile_attributes.is_collidable:
                        current_tile.add_component(BoxCollider2D("Box"))

                    row.append(current_tile)
            map_tiles.append(row)

        return map_tiles
