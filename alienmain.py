#Libraries
import sys

import pygame

import random

from aliensettings import Settings

from ship import Ship

from bullet import Bullet
#-------------------------------------------------------------------#

class AlienInvasion:

    def __init__(self):

        #Load stuff / using init()

        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().width
        
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()

    #Rungame func
    def run_game(self):
        #While loop/mainloop
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60)

#------------------------------------------------------------------------------------------------------------------------------------------------------#

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.sfx_click(event)
                

    def _check_keydown_events(self, event):       

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
                                                        #These statements take whether the key is pressed or let go to then another statement identifying the key then making the ship move
        elif event.key == pygame.K_LEFT:        
            self.ship.moving_left = True

        elif event.key == pygame.K_q:
            sys.exit()

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False                
                    
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        #Create a new bullet and group it to the bullet group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
        

    def sfx_click(self, event):
        num = random.randint(1,25)
        if num == 8:
            sfx = pygame.mixer.music.load("fart-with-reverb.mp3")
            pygame.mixer.music.play()


    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        pygame.display.flip()

#------------------------------------------------------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
