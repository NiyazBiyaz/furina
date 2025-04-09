import pygame as pg


# Дублирую чтобы просто работало, хз
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)


class Level(pg.sprite.Group):

    def __init__(self, map: str, chunk_size):
        # Инициализация уровня
        self.ground = pg.sprite.Group() # Группа для чанков земли
        self.walls  = pg.sprite.Group() # Группа для чанков стен
        for y, line in enumerate(map.split("\n")): # Потом поменять на чтение из json-конфига
            for x, chunk in enumerate(line.split()):

                ### Костыль
                GREEN_SURF = pg.Surface((chunk_size, chunk_size))
                GREEN_SURF.fill(GREEN)
                RED_SURF   = pg.Surface((chunk_size, chunk_size), masks=RED)
                RED_SURF.fill(RED)
                CHUNK_SQUARE = (chunk_size, chunk_size)
                ###
                
                if chunk == "0": # Чанк `0` - земля 
                    chunk = Chunk(GREEN_SURF, pg.Rect((chunk_size * x, chunk_size * y), CHUNK_SQUARE), self.ground)

                elif chunk == "1": # Чанк `1` - стены 
                    chunk = Chunk(RED_SURF, pg.Rect((chunk_size * x, chunk_size * y), CHUNK_SQUARE), self.walls)
            
        self.obstacles = pg.sprite.Group(self.walls.sprites())

        super().__init__(self.ground.sprites(), self.walls.sprites())


class Chunk(pg.sprite.Sprite):

    def __init__(self, image:pg.Surface, rect: pg.Rect, *groups):
        super().__init__(groups)
        self.image = image
        self.rect  = rect
