import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    
    def __init__(self, ai_game):

        super().__init__()

        #Set ships starting pos
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.settings = ai_game.settings

        #load Ship visuals
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()

        #Set position
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)
        #Moving boleans
        self.moving_right = False
        self.moving_left = False

        
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)


    def update(self):
        #move right
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        #move left
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
            
        self.rect.x = self.x


    def blitme(self):
        #Draw ship at the location
        self.screen.blit(self.image, self.rect)