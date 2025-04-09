import pygame
from pygame.event import Event


START_GAME = pygame.USEREVENT + 1


def _post_event(event):
    pygame.event.post(event)


def back() -> None:
    _post_event(Event(pygame.QUIT))

def start_game() -> None:
    _post_event(Event(START_GAME))
