#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.image
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import WIN_WIDTH, COLOR_CYAN, MENU_OPTION, COLOR_WHITE


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/MenuBg.png')  # Background for Menu
        self.rect = self.surf.get_rect(left=0, top=0)  # Left and top = 0, just to be sure Default

    def run(self, ):
        pygame.mixer_music.load('./asset/MenuSong.mp3')  # Song for Menu
        pygame.mixer_music.play(-1)  # Song always playing
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(50, "Sky", COLOR_CYAN, ((WIN_WIDTH / 2), 50))  # Customization Sky
            self.menu_text(50, "Shooter", COLOR_CYAN, ((WIN_WIDTH / 2), 100))

            # for i in range options in menu customization
            for i in range(len(MENU_OPTION)):
                self.menu_text(30, MENU_OPTION[i], COLOR_WHITE, ((WIN_WIDTH / 2), 200 + 32 * i))

            pygame.display.flip()

            # Check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Close Window
                    quit()  # End pygame

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Times New Roman", size=text_size)  # text size and font
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
