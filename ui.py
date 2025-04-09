import pygame as pg


# Button class, at this time need to expand
class Button(pg.sprite.Sprite):

    def __init__(self, image: pg.Surface, center: tuple[int, int], callback, *groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.callback = callback


    def update(self, cursor: pg.sprite.Sprite, activate: bool):
        if pg.sprite.collide_rect(self, cursor):
            if activate:
                self.callback()
