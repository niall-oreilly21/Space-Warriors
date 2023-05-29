from queue import Queue

from Engine.Other.Enums.EventEnums import EventCategoryType


class EventDispatcher:
    def __init__(self):
        self.listeners = {}
        self.event_queue = Queue()
        self.previous_event = None

    def add_listener(self, event_type, callback, event_data=None):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append((callback, event_data))

    def remove_listener(self, event_type, callback):
        if event_type in self.listeners:
            self.listeners[event_type].remove(callback)

    def dispatch_event(self, event_data):
        self.event_queue.put(event_data)

    def process_events(self):
        while not self.event_queue.empty():
            event_data = self.event_queue.get()
            if event_data == self.previous_event:
                continue  # Skip processing the same event multiple times
            self.previous_event = event_data
            event_type = event_data.event_category_type
            if event_type in self.listeners:
                callbacks = self.listeners[event_type].copy()  # Make a copy to iterate over
                for callback, registered_event_data in callbacks:
                    callback(event_data)
