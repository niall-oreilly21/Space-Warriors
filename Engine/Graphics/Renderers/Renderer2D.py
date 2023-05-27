from abc import abstractmethod

from Engine.GameObjects.Components.Component import Component


class Renderer2D(Component):
        def __init__(self, name, material, layer=0):
            super().__init__(name)
            self._material = material
            self._layer = layer

        @property
        def material(self):
            return self._material

        @property
        def layer(self):
            return self._layer

        def draw(self, surface, transform):
            self._material.draw(surface, transform)

        def clone(self):
            return Renderer2D(self._name, self._material.clone(), self._layer)