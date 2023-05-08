from Engine.GameObjects.GameObject import GameObjectType

class Scene:
    def __init__(self, name):
        self.name = name
        self.game_object_list = {
            GameObjectType.Static: {},
            GameObjectType.Dynamic: {},
            }

    def add(self, game_object):
        if game_object.category not in self.game_object_list[game_object.type]:
            self.game_object_list[game_object.type][game_object.category] = []
            self.game_object_list[game_object.type][game_object.category].append(game_object)

    def remove(self, game_object):
        if game_object.type in self.game_object_list[game_object.category]:
            self.game_object_list[game_object.type][game_object.category].remove(game_object)

    def find_all_by_type(self, type):
        result = []
        for category in self.game_object_list[type]:
            result.extend(self.game_object_list[type][category])
        return result

    def find_all_by_category(self, type, category):
        if category in self.game_object_list[type]:
            return self.game_object_list[type][category]
        else:
            return []

    def remove_all_by_category(self, type, category):
        if category in self.game_object_list[type]:
            return self.game_object_list[type].remove(category)
        else:
            return []

    def update(self, game_time):
        for type in self.game_object_list.values():
            for category in type.values():
                for game_object in category:
                    game_object.update(game_time)

    def get_all_components_by_type(self, component_type):
        all_components_by_type = []
        for type in self.game_object_list.values():
            for category in type.values():
                for game_object in category:
                    all_components_by_type.append(game_object.get_component(component_type))
        return all_components_by_type

    def render(self, screen, game_time):
        for type in self.game_object_list.values():
            for category in type.values():
                for game_object in category:
                    game_object.render(screen, game_time)

