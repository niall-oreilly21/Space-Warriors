from abc import abstractmethod

from Component import Component


class Renderer2D(Component):
        def __init__(self,name, material):
            super().__init__(name)
            self.material = material
            print(material.color)

        @abstractmethod
        def draw(self, surface):
            self.material.draw(surface, self.parent.transform)

