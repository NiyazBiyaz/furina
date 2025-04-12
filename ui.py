import pygame as pg
from events import EventListener


# Button class, at this time need to expand
class Button(pg.sprite.Sprite, EventListener):

    def __init__(self, image: pg.Surface, 
                 center: tuple[int, int], 
                 cursor: pg.sprite.Sprite,
                 on_activate,
                 event_bus,
                 *groups: pg.sprite.Group):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.on_activate = on_activate
        self.cursor = cursor
        self.activate = False
        super().register(pg.MOUSEBUTTONDOWN, event_bus)


    def update(self):
        if self.activate:
            self.activate = False
            self.on_activate()


    def callback(self, event: pg.event.Event):
        if event.button == pg.BUTTON_LEFT:
            if pg.sprite.collide_rect(self, self.cursor):
                self.activate = True
