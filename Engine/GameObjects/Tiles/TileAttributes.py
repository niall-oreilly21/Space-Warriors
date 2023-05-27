class TileAttributes:
    def __init__(self, tile_id, is_collidable = False, color=None, alpha=None):
        self.__tile_id = tile_id
        self.__is_collidable = is_collidable
        self.__color = color
        self.__alpha = alpha


    @property
    def tile_id(self):
        return self.__tile_id

    @property
    def is_collidable(self):
        return self.__is_collidable

    @property
    def color(self):
        return self.__color


    @property
    def alpha(self):
        return self.__alpha
