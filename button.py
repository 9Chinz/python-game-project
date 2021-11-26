import pygame, sys
from config import *

class Button:
    def __init__(self, text, color, width, height, pos, elevation, font_size = 24):
        self.color = color
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elev = elevation
        self.original_y_pos = pos[1]
        self.gui_font = pygame.font.Font(MINECRAFT_FONT, font_size)
        
        # top rect
        self.top_rect = pygame.Rect((pos), (width, height))
        self.top_rect.center = pos
        self.top_color = color
        
        #bottom rect
        self.bottom_rect = pygame.Rect((pos), (width, elevation))
        self.bottom_color = color
        
        # text
        self.text_surf = self.gui_font.render(text, True, WHITE)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)  
        
    def draw(self, screen):
        # specify elev logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elev
        self.text_rect.center = self.top_rect.center
        
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elev
        
        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        
    
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = GREY
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elev = 0
                self.pressed = True
            else:
                self.dynamic_elev = self.elevation
                if self.pressed:
                    self.pressed = False
                    return True
        else:
            self.dynamic_elev = self.elevation
            self.top_color = self.color
            self.pressed = False