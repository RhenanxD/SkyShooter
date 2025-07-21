# Const.py: Stores universal values and properties
import pygame

# C
# Menu Theme Color, if you want to change the color, just change the numbers inside the parameters
COLOR_CYAN = (0, 255, 255)  # Title Menu Text
COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (64, 178, 245)

# E
# Speed of everything
EVENT_ENEMY = pygame.USEREVENT + 1
ENTITY_SPEED = {
    'Level1Bg0': 0,
    'Level1Bg1': 1,
    'Level1Bg2': 2,
    'Level1Bg3': 3,
    'Level1Bg4': 4,
    'Level1Bg5': 5,
    'Player': 3,
    'Enemy1': 2,
    'Enemy2': 1,
}

ENTITY_HEALTH = {
    'Level1Bg0': 999,
    'Level1Bg1': 999,
    'Level1Bg2': 999,
    'Level1Bg3': 999,
    'Level1Bg4': 999,
    'Level1Bg5': 999,
    'Player': 300,
    'Enemy1': 50,
    'Enemy2': 60,
}

# M

MENU_OPTION = ('NEW GAME',
               'HARDCORE - MODE',
               'NO HIT - CHALLENGE',
               'SCORE',
               'QUIT')

# S
SPAWN_TIME = 3000

# W
# Screen Width and Height, change automatically to Game.py
WIN_WIDTH = 576
WIN_HEIGHT = 324
