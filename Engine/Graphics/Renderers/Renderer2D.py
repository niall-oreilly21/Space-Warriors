from abc import abstractmethod

from Engine.GameObjects.Components.Component import Component


class Renderer2D(Component):
        def __init__(self,name, material):
            super().__init__(name)
            self._material = material

        @property
        def material(self):
            return self._material

        def draw(self, surface, transform):
            self._material.draw(surface, transform)

