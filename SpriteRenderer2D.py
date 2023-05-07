from Renderer2D import Renderer2D
from SpriteAnimator2D import SpriteAnimator2D

class SpriteRenderer2D(Renderer2D):
    def __init__(self, name, material, sprite=None):
        super().__init__(name, material)
        self._sprite = sprite

    def draw(self, surface):
        sprite = self.parent.get_component(SpriteAnimator2D).get_current_sprite()
        if sprite:
            self.material.texture = sprite.texture
            self.material.source_rect = sprite.source_rect
            self.material.color = sprite.color
            self.material.origin = sprite.pivot
            self.material.draw(surface, self.parent.transform)




