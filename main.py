import pygame as pg


WIDTH, HEIGHT = 800, 600
FPS = 144

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)


START_GAME = pg.USEREVENT + 1


LEVEL = \
"""1 1 1 1 1 1 1 1
1 0 0 1 0 0 0 1
1 0 1 0 1 1 0 1
1 0 1 0 0 1 0 1
1 0 0 0 0 0 0 1
1 1 1 1 1 1 1 1
"""
CHUNK_SIZE = 100


def main():
    pg.init()

    # Initialize main window
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Stupid chicken Iskander")


    font = pg.font.Font("assets/fonts/PixelOperator.ttf", 32)


    resume = Button(font.render("Resume", True, BLACK), (400, 268), to_game)
    quit = Button(font.render("Exit Game", True, BLACK), (400, 300), back)
    menu_ui = pg.sprite.RenderUpdates(resume, quit)


    # Game objects (entities)
    players_group = pg.sprite.Group()
    player = Player(pg.Surface((50, 50)), pg.Rect(400, 300, 50, 50), 2)
    players_group.add(player)

    level = Level(LEVEL, CHUNK_SIZE)

    # Gameloop helpers
    state = "MENU"
    cursor = Cursor()
    cursor_activate = False
    clock = pg.time.Clock()
    running = True
    # Gameloop
    while running:
        # EXPAND TO STATES AND INPUT HANDLER
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == START_GAME:
                state = "GAME"
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 0:
                    cursor_activate = False
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    cursor_activate = True
        keys = pg.key.get_pressed()
        players_group.update(keys, level.obstacles)

        # Rendering
        screen.fill(WHITE)
        
        if state == "MENU":
            cursor.update()
            menu_ui.update(cursor, cursor_activate)
            menu_ui.draw(screen)
        elif state == "GAME":
            level.ground. draw(screen)
            level.walls.  draw(screen)
            players_group.draw(screen)

        pg.display.flip()
        # Frames per second limit
        clock.tick(FPS)

    pg.quit()


def back():
    pg.event.post(pg.event.Event(pg.QUIT))

def to_game():
    pg.event.post(pg.event.Event(START_GAME))


class Cursor(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.rect = pg.rect.Rect(0, 0, 1, 1)
        self.rect.topleft = pg.mouse.get_pos()

    def update(self):
        self.rect.topleft = pg.mouse.get_pos()


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
            


class Level:

    def __init__(self, map: str, chunk_size):
        # Инициализация уровня
        self.ground = pg.sprite.Group() # Группа для чанков земли
        self.walls  = pg.sprite.Group() # Группа для чанков стен
        for y, line in enumerate(map.split("\n")):
            for x, chunk in enumerate(line.split()):
                if chunk == "0":
                    chunk = pg.sprite.Sprite(self.ground) # Чанк `0` - земля
                    # Инициализация спрайта
                    chunk.image = pg.Surface((chunk_size, chunk_size))
                    chunk.rect  = chunk.image.get_rect()
                    chunk.rect.topleft = x * chunk_size, y * chunk_size

                    chunk.image.fill(GREEN) # Цвет зеленый

                elif chunk == "1":
                    chunk = pg.sprite.Sprite(self.walls) # Чанк `1` - стены 
                    # Инициализация спрайта
                    chunk.image = pg.Surface((chunk_size, chunk_size))
                    chunk.rect  = chunk.image.get_rect()
                    chunk.rect.topleft = x * chunk_size, y * chunk_size

                    chunk.image.fill(RED) # Цвет красный
            
        self.obstacles = pg.sprite.Group(self.walls.sprites())


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


if __name__ == "__main__":
    main()
