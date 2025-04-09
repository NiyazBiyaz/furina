import pygame as pg
from entities import Player
from ui import Button
from level import Level
from state_utils import back, start_game, START_GAME


WIDTH, HEIGHT = 800, 600
FPS = 144

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)


LEVEL = \
"""1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1
1 0 1 1 1 0 1 0 1 1 1 1 1 1 0 1
1 0 1 0 0 0 1 0 0 0 0 0 0 1 0 1
1 0 1 0 1 1 1 1 1 1 1 1 0 1 0 1
1 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1
1 0 1 1 1 1 1 1 1 1 0 1 1 1 0 1
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1
1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1
1 0 1 1 1 0 1 0 1 1 1 1 1 1 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
"""
CHUNK_SIZE = 50


def main():
    pg.init()

    # Initialize main window
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Stupid chicken Iskander")


    # Load font
    font = pg.font.Font("assets/fonts/PixelOperator.ttf", 32)

    ### Initialize States
    # Main menu elements
    resume = Button(font.render("Play", True, BLACK), (400, 268), start_game)
    quit = Button(font.render("Exit Game", True, BLACK), (400, 300), back)
    menu_ui = pg.sprite.Group(resume, quit)

    menu = GroupContainer(menu_ui)


    # Game objects (entities)
    players_group = pg.sprite.Group()
    player = Player(pg.Surface((26, 26)), pg.Rect(50, 50, 25, 25), 2)
    players_group.add(player)
    level = Level(LEVEL, CHUNK_SIZE)

    game = GroupContainer(level, players_group)

    state = "MENU"

    # Gameloop helpers
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
        cursor.update()

        # Clean screen
        screen.fill(WHITE)
        
        # States manager prototype
        if state == "MENU":
            menu.update(cursor, cursor_activate)
            menu.draw(screen)
        elif state == "GAME":
            game.update(keys, level.obstacles)
            game.draw(screen)

        pg.display.flip()
        # Frames per second limit
        clock.tick(FPS)

    pg.quit()


# Pseudo-cursor (at this moment, for ui collisions)
class Cursor(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.rect = pg.rect.Rect(0, 0, 1, 1)
        self.rect.topleft = pg.mouse.get_pos()

    def update(self):
        self.rect.topleft = pg.mouse.get_pos()


class GroupContainer:

    def __init__(self, *groups: pg.sprite.Group):
        self._groups = groups

    def update(self, *args):
        for grp in self._groups:
            grp.update(*args)

    def draw(self, screen: pg.Surface):
        for grp in self._groups:
            grp.draw(screen)


if __name__ == "__main__":
    main()
