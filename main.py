import pygame as pg


WIDTH, HEIGHT = 800, 600
FPS = 144

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)


LEVEL = (
    "1 1 1 1 1 1 1 1",
    "1 0 0 1 0 0 0 1",
    "1 0 1 0 1 1 0 1",
    "1 0 1 0 0 1 0 1",
    "1 0 0 0 0 0 0 1",
    "1 1 1 1 1 1 1 1",
)
CHUNK_SIZE = 100


def main():
    pg.init()

    # Initialize main window
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Stupid chicken Iskander")


    # Game objects (entities)
    players_group = pg.sprite.Group()
    player = Player(pg.Surface((50, 50)), pg.Rect(400, 300, 50, 50), 2)
    players_group.add(player)


    # Инициализация уровня
    ground = pg.sprite.Group() # Группа для чанков земли
    walls  = pg.sprite.Group() # Группа для чанков стен
    for y, line in enumerate(LEVEL):
        for x, chunk in enumerate(line.split()):
            if chunk == "0":
                chunk = pg.sprite.Sprite(ground) # Чанк `0` - земля
                # Инициализация спрайта
                chunk.image = pg.Surface((CHUNK_SIZE, CHUNK_SIZE))
                chunk.rect  = chunk.image.get_rect()
                chunk.rect.topleft = x * CHUNK_SIZE, y * CHUNK_SIZE

                chunk.image.fill(GREEN) # Цвет зеленый

            elif chunk == "1":
                chunk = pg.sprite.Sprite(walls) # Чанк `1` - стены 
                # Инициализация спрайта
                chunk.image = pg.Surface((CHUNK_SIZE, CHUNK_SIZE))
                chunk.rect  = chunk.image.get_rect()
                chunk.rect.topleft = x * CHUNK_SIZE, y * CHUNK_SIZE

                chunk.image.fill(RED) # Цвет красный
    
    obstacles = pg.sprite.Group(walls.sprites())

    # Gameloop helpers
    clock = pg.time.Clock()
    running = True
    # Gameloop
    while running:
        # EXPAND TO STATES AND INPUT HANDLER
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        keys = pg.key.get_pressed()
        players_group.update(keys, obstacles)

        # Rendering
        screen.fill(WHITE)
        
        ground.draw(screen)
        walls. draw(screen)
        players_group.draw(screen)

        pg.display.flip()
        # Frames per second limit
        clock.tick(FPS)

    pg.quit()


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
        
        # делаем движение, если оно заставляет нас столкнуться с препятствием возвращаем прошлое
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


if __name__ == "__main__":
    main()
