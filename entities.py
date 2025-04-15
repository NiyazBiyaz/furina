import pygame as pg
from events import EventListener

# Класс игрока
class Player(pg.sprite.Sprite, EventListener):

    def __init__(self, image: pg.Surface, 
                 rect: pg.Rect, 
                 speed: int, 
                 event_bus,
                 obstacles: pg.sprite.Group):
        super().__init__()
        self.image  = image
        self.rect   = rect
        self._speed = speed # Скорость изменения координат
        self._move_x = 0
        self._move_y = 0
        self.obstacles = obstacles

        super().registermany(event_bus,
                                   pg.KEYDOWN,
                                   pg.KEYUP  ,)
        

    def update(self):        
        # сохраняем прошлые координаты
        prev_left = self.rect.left
        prev_top = self.rect.top

        # делаем движение, если оно заставляет нас столкнуться с препятствием возвращаем обратно
        self.rect.left += self._move_x
        if pg.sprite.spritecollideany(self, self.obstacles):
            self.rect.left = prev_left
        
        self.rect.centery += self._move_y
        if pg.sprite.spritecollideany(self, self.obstacles):
            self.rect.top = prev_top


    def handle_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            match event.scancode:
                case pg.KSCAN_W:
                    self._move_y -= self._speed
                case pg.KSCAN_A:
                    self._move_x -= self._speed
                case pg.KSCAN_S:
                    self._move_y += self._speed
                case pg.KSCAN_D:
                    self._move_x += self._speed
        elif event.type == pg.KEYUP:
            match event.scancode:
                case pg.KSCAN_W:
                    self._move_y += self._speed
                case pg.KSCAN_A:
                    self._move_x += self._speed
                case pg.KSCAN_S:
                    self._move_y -= self._speed
                case pg.KSCAN_D:
                    self._move_x -= self._speed
        else:
            raise ValueError(f"Invalid event type! Recieved: {event.type}")
