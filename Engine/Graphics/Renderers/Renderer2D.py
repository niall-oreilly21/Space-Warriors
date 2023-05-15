from abc import abstractmethod

from Engine.GameObjects.Components.Component import Component


class Renderer2D(Component):
        def __init__(self,name, material):
            super().__init__(name)
            self._material = material

        @abstractmethod
        def draw(self, surface):
            self._material.draw(surface, self.parent.transform)

