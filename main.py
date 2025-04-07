import pygame as pg


WIDTH, HEIGHT = 800, 600
FPS = 144

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)


def main():
    pg.init()

    # Initialize main window
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Stupid chicken Iskander")


    # Game objects (entities)
    players_group = pg.sprite.Group()
    player = pg.sprite.Sprite()
    player.image = pg.Surface((50, 50))
    player.rect = player.image.get_rect()
    player.speed = 2
    players_group.add(player)


    # Gameloop helpers
    clock = pg.time.Clock()
    running = True
    # Gameloop
    while running:
        # EXTERN TO STATES AND INPUT-HANDLER
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            player.rect.centery -= 1
        if keys[pg.K_a]:
            player.rect.centerx -= 1
        if keys[pg.K_s]:
            player.rect.centery += 1
        if keys[pg.K_d]:
            player.rect.centerx += 1

        # Rendering
        screen.fill(WHITE)
        
        players_group.draw(screen)

        pg.display.flip()
        # Frames per second limit
        clock.tick(FPS)


if __name__ == "__main__":
    main()