from Engine.GameObjects.GameObject import GameObjectType


class Scene:
    def __init__(self, name):
        self.__name = name
        self.__game_object_list = {
            GameObjectType.Static: {},
            GameObjectType.Dynamic: {},
        }

    @property
    def name(self):
        return self.__name

    def add(self, game_object):
        if game_object.game_object_category not in self.__game_object_list[game_object.game_object_type]:
            self.__game_object_list[game_object.game_object_type][game_object.game_object_category] = []

        self.__game_object_list[game_object.game_object_type][game_object.game_object_category].append(game_object)

    def remove(self, game_object):
        if game_object.game_object_category in self.__game_object_list[game_object.game_object_type]:
            return self.__game_object_list[game_object.game_object_type][game_object.game_object_category].remove(
                game_object)
        else:
            return False

    def find_all_by_type(self, game_object_type):
        result = []
        for game_object_category in self.__game_object_list[game_object_type]:
            result.extend(self.__game_object_list[game_object_type][game_object_category])
        return result

    def find_all_by_category(self, game_object_type, game_object_category):
        if game_object_category in self.__game_object_list[game_object_type]:
            return self.__game_object_list[game_object_type][game_object_category]
        else:
            return []

    def remove_all_by_category(self, game_object_type, game_object_category):
        if game_object_category in self.__game_object_list[game_object_type]:
            return self.__game_object_list[game_object_type].pop(game_object_category)
        else:
            return []

    def get_all_components_by_type(self, component_type):
        all_components_by_type = []
        for game_object_type in self.__game_object_list.values():
            for game_object_category in game_object_type.values():
                for game_object in game_object_category:
                    components = game_object.get_components(component_type)
                    all_components_by_type.extend(components)
        return all_components_by_type

    def contains(self, game_object):
        for game_object_type in self.__game_object_list.values():
            for game_object_category in game_object_type.values():
                if game_object in game_object_category:
                    return True
        return False

    def update(self, game_time):
        for game_object_type in list(self.__game_object_list.values()):
            for game_object_category in list(game_object_type.values()):
                for game_object in list(game_object_category):
                    game_object.update(game_time)

    def start(self):
        for game_object_type in self.__game_object_list.values():
            for game_object_category in game_object_type.values():
                for game_object in game_object_category:
                    game_object.start()
