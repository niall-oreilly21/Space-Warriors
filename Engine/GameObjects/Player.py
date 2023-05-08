from Engine.GameObjects.GameObject import GameObject

class Player(GameObject):
    def __init__(self, name, transform, type, category):
        super().__init__(name, transform, type, category)
