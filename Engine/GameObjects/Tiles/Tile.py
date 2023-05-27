# Create a tile game object class
from Engine.GameObjects.GameObject import GameObject
from Engine.Graphics.Materials.TextureMaterial2D import TextureMaterial2D
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Other.Enums.GameObjectEnums import GameObjectCategory, GameObjectType


class Tile(GameObject):
    def __init__(self, name, tile_id, position_on_sprite_sheet, transform=None, game_object_type=GameObjectType.Static,  game_object_category=GameObjectCategory.Tile):
        super().__init__(name, transform, game_object_type, game_object_category)

        self.renderer = self.get_component(Renderer2D)
        self.__tile_id = tile_id
        self.__position_on_sprite_sheet = position_on_sprite_sheet

    @property
    def tile_id(self):
        return self.__tile_id

    @property
    def position_on_sprite_sheet(self):
        return self.__position_on_sprite_sheet

    def clone(self):
        tile = Tile(self.name, self.tile_id, self.position_on_sprite_sheet, self.transform.clone(), self.game_object_type, self.game_object_category)

        for component in self._components:
            cloned_component = component.clone()
            tile.add_component(cloned_component)

        return tile
