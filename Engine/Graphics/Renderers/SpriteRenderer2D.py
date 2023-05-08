from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Graphics.Sprites.SpriteAnimator2D import SpriteAnimator2D

class SpriteRenderer2D(Renderer2D):
    def __init__(self, name, material, sprite=None):
        super().__init__(name, material)
        self._sprite = sprite
        self.flip_x = False
        self.flip_y = False

    def draw(self, surface):
        sprite = self.parent.get_component(SpriteAnimator2D).get_current_sprite()

        if sprite:
            self.material.texture = sprite.texture
            self.material.source_rect = sprite.source_rect
            self.material.color = sprite.color
            self.material.origin = sprite.pivot
            self.material.flip_x = self.flip_x
            self.material.flip_y = self.flip_y
            self.material.draw(surface, self.parent.transform)





