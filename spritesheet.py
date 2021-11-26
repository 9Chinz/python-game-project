import pygame

class SpriteSheet():
    def __init__(self, image, width, height, scale = 3):
        self.sheet = image
        self.scale = scale
        self.width = width
        self.height = height
        
    def get_img(self, frame, row, deg = 0):
        image = pygame.Surface((self.width, self.height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * self.width), (row * self.height), self.width, self.height))
        image = pygame.transform.rotate(image, deg)
        image = pygame.transform.scale(image, (self.width * self.scale, self.height * self.scale))
        image.set_colorkey((0, 0, 0))
        return image