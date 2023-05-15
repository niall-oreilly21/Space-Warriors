from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D

class SpriteRenderer2D(Renderer2D):
    def __init__(self, name, material, sprite=None):
        super().__init__(name, material)
        self.__sprite = sprite
        self.__flip_x = False
        self.__flip_y = False

    @property
    def flip_x(self):
        return self.__flip_x

    @property
    def flip_y(self):
        return self.__flip_y

    @flip_x.setter
    def flip_x(self, flip_x):
        self.__flip_x = flip_x

    @flip_y.setter
    def flip_y(self, flip_y):
        self.__flip_y = flip_y

    def draw(self, surface):
        sprite = self.parent.get_component(SpriteAnimator2D).get_current_sprite()

        if sprite:
            self._material.texture = sprite.texture
            self._material.source_rect = sprite.source_rect
            self._material.color = sprite.color
            self._material.origin = sprite.pivot
            self._material.flip_x = self.__flip_x
            self._material.flip_y = self.__flip_y
            self._material.draw(surface, self.parent.transform)





