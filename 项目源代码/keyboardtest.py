import pygame
from alien_invasion import AlienInvasion


def test_keydown_event_moving_right():
    ai_game = AlienInvasion()
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
    ai_game._check_keydown_events(event)

    assert ai_game.ship.moving_right is True


def test_keydown_event_moving_left():
    ai_game = AlienInvasion()
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
    ai_game._check_keydown_events(event)


    assert ai_game.ship.moving_left is True


def test_keydown_event_moving_up():
    ai_game = AlienInvasion()
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
    ai_game._check_keydown_events(event)

    assert ai_game.ship.moving_up is True


def test_keydown_event_moving_down():
    ai_game = AlienInvasion()
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
    ai_game._check_keydown_events(event)

    assert ai_game.ship.moving_down is True