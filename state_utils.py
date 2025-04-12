import pygame
from pygame.event import Event


STATE_CHANGE = pygame.event.custom_type()


def _post_event(event):
    pygame.event.post(event)


def back() -> None:
    _post_event(Event(pygame.QUIT))

def to_game() -> None:
    _post_event(Event(STATE_CHANGE, direct="GAME"))

def to_menu() -> None:
    _post_event(Event(STATE_CHANGE, direct="MENU"))
