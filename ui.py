from config import *
from button import Button
import pygame

class HealthBorder(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health_border = pygame.image.load(HEALTH_BAR_BORDER_IMG).convert_alpha()
        self.image = pygame.transform.scale(self.health_border, (self.health_border.get_width() * IMG_SCALE, self.health_border.get_height() * IMG_SCALE))
        self.rect = self.health_border.get_rect(bottomleft = (10, WINDOW_HEIGHT-55))

class GameUI(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health_img = pygame.image.load(HEALTH_BAR).convert_alpha()
        self.health_img = pygame.transform.scale(self.health_img, (self.health_img.get_width() * IMG_SCALE, self.health_img.get_height() * IMG_SCALE))
        self.health_img_rect = self.health_img.get_rect(bottomleft = (66, WINDOW_HEIGHT-4))
        self.max_health = self.health_img.get_width()
        self.health_amount = 0
        self.multiplier_score = 1
        self.score = 0
        
        self.popup_botton = Button("menu", GREEN, 100, 30, (55, 10), 6, 16)
        self.health_pack = pygame.sprite.Group()
        self.health_border = HealthBorder()
        self.health_pack.add(self.health_border)
        self.score_font = pygame.font.Font(MINECRAFT_FONT, 32)
        self.mulitple_font = pygame.font.Font(MINECRAFT_FONT, 28)
        self.lives_font = pygame.font.Font(MINECRAFT_FONT, 24)
        
    
    def draw(self, screen):
        self.popup_botton.draw(screen)
        self.health_pack.draw(screen)
        score_text = self.score_font.render(f"Score {self.score}", True, WHITE)
        score_text_rect = score_text.get_rect(bottomright = (WINDOW_WIDTH - 10, WINDOW_HEIGHT - 10))
        multi_score_text = self.mulitple_font.render(f"{self.multiplier_score} X ", True, WHITE)
        multi_score_rect = multi_score_text.get_rect(midright = score_text_rect.midleft)
        lives_text = self.lives_font.render(f"{int(self.health_amount/DAMAGE)}", True, WHITE)
        lives_rect = lives_text.get_rect(center = (self.health_img_rect.midleft[0]-21, self.health_img_rect.midleft[1]-3))
        
        screen.blit(score_text, score_text_rect)
        screen.blit(multi_score_text, multi_score_rect)
        screen.blit(self.health_img, self.health_img_rect, (0, 0, self.health_amount, 100))
        screen.blit(lives_text, lives_rect)

class OptionMenu:
    def __init__(self):
        self.box = pygame.Rect(0, 0, 300, 230)
        self.box.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.botton_resume = Button("Continue", GREEN, 130, 40, (self.box.centerx, self.box.centery - 10), 6, 16)
        self.botton_exit = Button("Exit", RED, 130, 40, (self.box.centerx, self.box.centery + 50), 6, 16)
        self.score_font = pygame.font.Font(MINECRAFT_FONT, 26)
        
    def draw(self, screen, score):
        pygame.draw.rect(screen, WHITE, self.box, border_radius=12)
        self.draw_score(screen, score, "SCORE")
        self.botton_resume.draw(screen)
        self.botton_exit.draw(screen)
    
    def draw_game_over(self, screen, score):
        pygame.draw.rect(screen, WHITE, self.box, border_radius=12)
        self.draw_score(screen, score, "FINAL SCORE")
        self.botton_exit.draw(screen)
    
    def draw_score(self, screen, score, text):
        score_text = self.score_font.render(text+f" {score}", True, BLACK)
        score_text_rect = score_text.get_rect(center = (self.box.center[0], self.box.center[1] - 55))
        screen.blit(score_text, score_text_rect)