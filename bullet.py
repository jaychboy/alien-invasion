import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_game):
        #Create Bullet
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        
        self.rect.midtop = ai_game.ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        #Function moves bullet up the screen
        self.y -= self.settings.bullet_speed

        #Set (y cords)
        self.rect.y = self.y

    def draw_bullet(self):
        #Draw bullet with settings
        pygame.draw.rect(self.screen, self.color, self.rect)
