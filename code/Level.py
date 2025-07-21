
import random

import pygame.display
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import (C_WHITE, WIN_HEIGHT, EVENT_ENEMY, SPAWN_TIME, C_RED, EVENT_TIMEOUT, TIMEOUT_STEP, TIMEOUT_LEVEL,
                        MENU_OPTION)
from code.Enemy import Enemy
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Player import Player


class Level:
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int]):
        self.timeout = TIMEOUT_LEVEL
        self.window = window
        self.name = name
        self.game_mode = game_mode  # Game mode (New game, Hardcore, No hit)
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity(self.name + 'Bg'))
        player = EntityFactory.get_entity('Player')
        player.score = player_score[0]
        self.entity_list.append(player)
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)  # 100ms

        # Change game mode
        EntityMediator.set_game_mode(self.game_mode)

    def run(self, player_score: list[int]):
        pygame.mixer.music.load(f'./asset/{self.name}Song.mp3')  # Inserting song Level 1
        pygame.mixer_music.play(-1)  # Always playing song
        clock = pygame.time.Clock()  # Fps
        while True:
            clock.tick(60)
            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                ent.move()
                if isinstance(ent, (Player, Enemy)):  # Verify if shot exist or not
                    shoot = ent.shoot()
                    if shoot is not None:  # If shot doesn't exist don't return as parameter
                        self.entity_list.append(shoot)
                if ent.name == 'Player':
                    # Verifying condition for no hit game mode
                    if self.game_mode == MENU_OPTION[2] and ent.health <= 0:
                        print("You Lose - No Hit Mode")
                        return False
                    self.level_text(16, f'Player - Health: {ent.health}  |  Score: {ent.score}', C_RED, (10, 25))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == EVENT_ENEMY:
                    choice = random.choice(('Enemy1', 'Enemy2'))  # Random choice of enemy that will appear in the game
                    self.entity_list.append(EntityFactory.get_entity(choice))
                if event.type == EVENT_TIMEOUT:
                    self.timeout -= TIMEOUT_STEP
                    if self.timeout == 0:  # If the player pass the level, the level will continue
                        for ent in self.entity_list:
                            if isinstance(ent, Player) and ent.name == 'Player':
                                player_score[0] = ent.score
                        return True

            # Hud and Information Graphics
            self.level_text(16, f'{self.name} - Timeout: {self.timeout / 1000:.1f}s', C_WHITE, (10, 5))
            self.level_text(16, f'fps: {clock.get_fps():.0f}', C_WHITE, (10, WIN_HEIGHT - 35))
            self.level_text(16, f'entities: {len(self.entity_list)}', C_WHITE, (10, WIN_HEIGHT - 20))
            pygame.display.flip()
            EntityMediator.verify_collision(entity_list=self.entity_list)  # Verify collision
            EntityMediator.verify_health(entity_list=self.entity_list)  # Verify Health

            found_player = False
            for ent in self.entity_list:
                if isinstance(ent, Player):
                    found_player = True
                    break

            if not found_player:
                return False

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Times New Roman", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)
