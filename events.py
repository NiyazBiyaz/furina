import pygame as pg
from collections import defaultdict


class EventListener:

    def handle_event(self, event: pg.event.Event) -> None:
        """Overridable method for `EventBus` interface"""
        raise NotImplementedError(f"Override method '{self.handle_event.__name__}' in your class")
        

    def register(self, event: int, bus) -> None:
        bus.subscribe(event, self)

    
    def registermany(self, bus, *events: int) -> None:
        for event in events:
            self.register(event, bus)


class EventBus:

    def __init__(self):
        self.listeners = defaultdict(list)


    def subscribe(self, event: int, sub: EventListener):
        self.listeners[event].append(sub)

    
    def unsub(self, event: int, sub: EventListener):
        self.listeners[event].remove(sub)
        if len(self.listeners[event]) == 0:
            del self.listeners[event]


    def update(self):
        for event in pg.event.get():
            if event.type in self.listeners:
                self.dispatch(event)


    def dispatch(self, event: pg.event.Event):
        for listener in self.listeners[event.type]:
            listener.handle_event(event)
