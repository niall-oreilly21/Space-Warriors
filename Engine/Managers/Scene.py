from App.Constants.Application import Application
from App.Constants.Constants import Constants
from Engine.GameObjects.Components.Physics.BoxCollider2D import BoxCollider2D
from Engine.GameObjects.GameObject import GameObjectType
from Engine.Graphics.Renderers.Renderer2D import Renderer2D
from Engine.Managers.EventSystem.EventData import EventData
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType


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

        if Application.GameStarted is True:
            self.__dispatch_quad_tree_add_events(game_object)
        self.__game_object_list[game_object.game_object_type][game_object.game_object_category].append(game_object)

    def __dispatch_quad_tree_remove_events(self, game_object):
        if game_object.get_component(BoxCollider2D):
            Constants.EVENT_DISPATCHER.dispatch_event(
                EventData(EventCategoryType.CollisionManager, EventActionType.RemoveColliderFromQuadTree, [game_object.get_component(BoxCollider2D)]))

        for renderer in game_object.get_components(Renderer2D):
            Constants.EVENT_DISPATCHER.dispatch_event(
                EventData(EventCategoryType.RendererManager, EventActionType.RemoveRendererFromQuadTree,
                          [renderer]))

    def __dispatch_quad_tree_add_events(self, game_object):
        if game_object.get_component(BoxCollider2D):
            Constants.EVENT_DISPATCHER.dispatch_event(
                EventData(EventCategoryType.CollisionManager, EventActionType.AddColliderToQuadTree,
                          [game_object.get_component(BoxCollider2D)]))

            for renderer in game_object.get_components(Renderer2D):
                Constants.EVENT_DISPATCHER.dispatch_event(
                    EventData(EventCategoryType.RendererManager, EventActionType.AddRendererToQuadTree,
                              [renderer]))


    def remove(self, game_object):
        if game_object.game_object_category in self.__game_object_list[game_object.game_object_type]:

            if Application.GameStarted is True:
                self.__dispatch_quad_tree_remove_events(game_object)
            return self.__game_object_list[game_object.game_object_type][game_object.game_object_category].remove(game_object)
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
