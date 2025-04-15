import pygame as pg
from entities import Player
from ui import Button
from level import Level
from state_utils import back, to_game, to_menu, STATE_CHANGE
from events import EventBus, EventListener


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

    event_bus = EventBus()
    cursor = Cursor()

    # Load font
    font = pg.font.Font("assets/fonts/PixelOperator.ttf", 32)

    ### Initialize States
    # Main menu elements
    resume = Button(font.render("Play", True, BLACK), (400, 268), cursor, to_game, event_bus)
    quit = Button(font.render("Exit Game", True, BLACK), (400, 300), cursor, back, event_bus)
    menu_ui = pg.sprite.Group(resume, quit)

    menu = GroupContainer(menu_ui)


    # Game objects (entities)
    level = Level(LEVEL, CHUNK_SIZE)
    players_group = pg.sprite.Group()
    player = Player(pg.Surface((26, 26)), pg.Rect(50, 50, 25, 25), 2, event_bus, level.obstacles)
    players_group.add(player)

    exit = Button(font.render("Main menu", True, BLACK), (80, 30), cursor, to_menu, event_bus)
    game_ui = pg.sprite.Group(exit)

    game = GroupContainer(level, players_group, game_ui)

    state_manager = StateManager("MENU", event_bus)

    # Gameloop helpers
    clock = pg.time.Clock()
    running = True

    # Gameloop
    while running:
        # EXPAND TO STATES AND INPUT HANDLER
        event_bus.update()
        cursor.update()

        running = state_manager.update()

        # Clean screen
        screen.fill(WHITE)
        
        # States manager prototype
        if state_manager.state == "MENU":
            menu.update()
            menu.draw(screen)
        elif state_manager.state == "GAME":
            game.update()
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


class StateManager(EventListener):

    def __init__(self, start_state: str, eventbus: EventBus):
        self.state = start_state
        self.running = True
        super().registermany(eventbus, 
                             pg.QUIT,
                             STATE_CHANGE)


    def update(self):
        return self.running


    def handle_event(self, event: pg.event.Event):
        if event.type == STATE_CHANGE:
            self.state = event.direct
        elif event.type == pg.QUIT:
            self.running = False


class GroupContainer:

    def __init__(self, *groups: pg.sprite.Group):
        if not groups:
            raise TypeError("At least one group is required!")
        self._groups = groups
        
    
    def draw(self, surface: pg.Surface, bgsurf: pg.Surface = None, special_flags: int = 0):
        for grp in self._groups:
            grp.draw(surface, bgsurf, special_flags)


    def update(self):
        for grp in self._groups:
            grp.update()


if __name__ == "__main__":
    main()
