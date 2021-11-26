import pygame
from button import Button
from config import *

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(MINECRAFT_FONT, 120)
        self.small_font = pygame.font.Font(MINECRAFT_FONT, 20)
        self.mid_font = pygame.font.Font(MINECRAFT_FONT, 48)
        
        self.creator_text = self.small_font.render(AUTHOR, True, (255, 255, 255))
        self.creator_text_rect = self.creator_text.get_rect(bottomleft = (10, WINDOW_HEIGHT-10))
        
        self.title = GAME_TITLE
        self.title_font = self.font.render(self.title, True, (255, 255, 255))
        self.title_font_shadow = self.font.render(self.title, True, (0, 0, 0))
        self.title_font_rect = self.title_font.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.2))
        self.title_font_shadow_rect = self.title_font_shadow.get_rect(center = (WINDOW_WIDTH / 2, (WINDOW_HEIGHT * 0.2)+10))
        
class SelectMenu(Menu):
    def __init__(self):
        super().__init__()
        self.easy_button = Button("Easy", GREEN, 200, 50, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 6, 24)
        self.hard_button = Button("Hard", PURPLE, 200, 50, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100), 6, 24)
        self.back_botton = Button("Go back", RED, 180, 40, (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.6 + 120), 6, 20)
    
    def draw(self, screen):
        #!! order the rendering
        screen.blit(self.title_font_shadow, self.title_font_shadow_rect)    
        screen.blit(self.title_font, self.title_font_rect)
        screen.blit(self.creator_text, self.creator_text_rect)
        self.easy_button.draw(screen)
        self.hard_button.draw(screen)
        self.back_botton.draw(screen)
        

class MainMenu(Menu):
    def __init__(self):
        super().__init__()        
        self.start_button = Button("Start", GREEN, 200, 50, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 6)
        self.exit_button = Button("Exit", RED, 200, 50, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100), 6)
        self.high_score = 0

    
    def draw(self, screen):
        #!! order the rendering
        text_score = self.mid_font.render(f"highest Score {self.high_score}", True, (255, 255, 255))
        text_score_rect = text_score.get_rect(bottomright = (WINDOW_WIDTH - 10, WINDOW_HEIGHT - 10))
        screen.blit(self.title_font_shadow, self.title_font_shadow_rect)    
        
        screen.blit(self.title_font, self.title_font_rect)
        screen.blit(self.creator_text, self.creator_text_rect)
        screen.blit(text_score, text_score_rect)
        self.start_button.draw(screen)
        self.exit_button.draw(screen)
    
    def set_higher_score(self, score):
        self.high_score = score
