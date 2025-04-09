import pygame as pg


# Класс игрока
class Player(pg.sprite.Sprite):

    def __init__(self, image: pg.Surface, rect: pg.Rect, speed: int):
        super().__init__()
        self.image  = image
        self.rect   = rect
        self._speed = speed # Скорость изменения координат
        self._move_x = 0
        self._move_y = 0


    def update(self, keys: list, obastacles: pg.sprite.Group):
        self._handle_keys(keys)
        
        # сохраняем прошлые координаты
        prev_left = self.rect.left
        prev_top = self.rect.top

        # делаем движение, если оно заставляет нас столкнуться с препятствием возвращаем прошлое
        self.rect.left += self._move_x
        if pg.sprite.spritecollideany(self, obastacles):
            self.rect.left = prev_left
        
        self.rect.centery += self._move_y
        if pg.sprite.spritecollideany(self, obastacles):
            self.rect.top = prev_top


    def _handle_keys(self, keys: list):
        # Обнуляем прошлые движения
        self._move_x = 0
        self._move_y = 0
        
        # Раскладка WASD
        if keys[pg.K_w]:
            self._move_y -= self._speed
        if keys[pg.K_a]:
            self._move_x -= self._speed
        if keys[pg.K_s]:
            self._move_y += self._speed
        if keys[pg.K_d]:
            self._move_x += self._speed
