class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.activeScene = None

    def add(self, id, scene):
        id = id.strip().lower()
        if id in self.scenes:
            return False
        self.scenes[id] = scene
        return True

    def set_active_scene(self, id):
        id = id.strip().lower()
        if id in self.scenes:
            self.activeScene = self.scenes[id]
        return self.activeScene

    def update(self, game_time):
        if  self.activeScene is not None:
            self.activeScene.update(game_time)
