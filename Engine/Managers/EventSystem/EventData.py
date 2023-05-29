class EventData:
    def __init__(self, event_category_type, event_action_type, parameters):
        self.__event_category_type = event_category_type
        self.__event_action_type = event_action_type
        self.__parameters = parameters

    @property
    def event_category_type(self):
        return self.__event_category_type

    @property
    def event_action_type(self):
        return self.__event_action_type

    @property
    def parameters(self):
        return self.__parameters