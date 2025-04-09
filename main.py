import pygame as pg
from entities import Player
from ui import Cursor, Button
from level import Level


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


    # Load font
    font = pg.font.Font("assets/fonts/PixelOperator.ttf", 32)


    # Main menu elements
    resume = Button(font.render("Play", True, BLACK), (400, 268), to_game)
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
        
        # States manager prototype
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


if __name__ == "__main__":
    main()
