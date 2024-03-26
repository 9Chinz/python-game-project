import pygame
from menu import SelectMenu, MainMenu
from game import Game
from config import *
import asyncio, sys, platform
from pygame.locals import DOUBLEBUF, FULLSCREEN

class MainGame:
    def __init__(self):
        self.state = 'main_menu'
        self.background = pygame.image.load(BACKGROUND_IMG).convert_alpha()
        self.background = pygame.transform.scale(self.background, (256*4, 608*4))
        self.background_rect = self.background.get_rect()
        self.bg_y = self.background_rect.y
        self.game_mode = "easy"
        self.bg_music = pygame.mixer.Sound(BACKGROUND_MUSIC)
        self.bg_music.set_volume(BG_VOLUME)

    def main_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game_menu.draw(screen)
        game_menu.set_higher_score(main_game.get_score()['high_score'])
            
        if game_menu.start_button.check_click():
            self.state = "select_level"
        if game_menu.exit_button.check_click():
            pygame.quit()
            sys.exit()
    
    def select_level(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "main_menu"
                
        select_menu.draw(screen)
        if select_menu.easy_button.check_click():
            self.bg_music.play(-1)
            self.game_mode = "easy"
            self.state = "main_game"
        if select_menu.hard_button.check_click():
            self.game_mode = "hard"
            self.bg_music.play(-1)
            self.state = "main_game"
        if select_menu.back_botton.check_click():
            self.state = "main_menu"
    
    async def main_game(self, mode):
        await main_game.main(screen, mode)
        if main_game.is_game_end:
            self.state = "main_menu"
            self.bg_music.stop()
            main_game.reset()
    
    async def menu_state(self):
        self.draw_background(screen)
        if self.state == "main_menu":
            self.main_menu()
        if self.state == "select_level":
            self.select_level()
        if self.state == "main_game":
            await self.main_game(self.game_mode)
    
    def draw_background(self, screen):
        # return remain y
        rel_y = self.bg_y % self.background_rect.width
        screen.blit(self.background, (0, rel_y - self.background_rect.width))
        if rel_y < WINDOW_HEIGHT:
            screen.blit(self.background, (0, rel_y))
        # update screen
        self.bg_y += 1

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF, 16)
pygame.mixer.pre_init(44100, 16, 2, 512)
pygame.display.set_caption(GAME_CAPTION)
pygame.display.set_icon(pygame.image.load(ICON_IMG).convert_alpha())

# obj create

game_menu = MainMenu()
select_menu = SelectMenu()
main_game = Game()
game = MainGame()

async def main():
    while True:
        await game.menu_state()
        pygame.display.update()
        await asyncio.sleep(0)
        clock.tick(FPS)
        
asyncio.run(main())