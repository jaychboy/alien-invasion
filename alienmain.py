#Libraries
import sys

import pygame

import random

from time import sleep

#-------------------------------------------------------------------#

#File imports


from ship import Ship

from bullet import Bullet

from alien import Alien

from button import Button

from scoreboard import Scoreboard

from game_stats import GameStats

from aliensettings import Settings



#-------------------------------------------------------------------#

#The holy function (AlienInvasion) :o 

         #  | #
         # \/#

class AlienInvasion:

    def __init__(self):

        #Load stuff / using init()

        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")

        self.game_active = False

        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()
        
        self.stats = GameStats(self)

        self.sb = Scoreboard(self)

        self.play_button = Button(self, "Play")

        self._create_fleet()


    #Rungame func
    def run_game(self):
        #While loop/mainloop
        while True:
            self._check_events()

            #Functions only active is game is running.
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

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
                mouse_pos = pygame.mouse.get_pos()      #Get mouse pos using get_pos(function)
                self._check_play_button(mouse_pos)

                self.sfx_click(event)

    def _check_play_button(self, mouse_pos):

        #If play_button collides with mouse_pos/where mouse is and game is not activve, game starts running

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.game_active:
            #random soundboard sfx :)
            
            wesfx = pygame.mixer.music.load("sfx/wedonotcare.mp3")
            pygame.mixer.music.play()

            self.stats.reset_stats()
            self.game_active = True

            #Prep text
            self.sb.prep_score()
            self.sb.prep_level()
            
            self.sb.prep_ships()

            #Few more functions in order to get game ready
            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

            self.settings.initialize_dynamic_settings()
                

    def _check_keydown_events(self, event):       

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
                                              #These statements take whether the key is pressed or let go to then another statement identifying the key then making the ship move.s
        elif event.key == pygame.K_LEFT:        
            self.ship.moving_left = True

        elif event.key == pygame.K_q:
            sys.exit()

        elif event.key == pygame.K_h:
            pygame.mouse.set_visible(False)
        
        elif event.key == pygame.K_j:
            pygame.mouse.set_visible(True)

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
            if self.game_active == True:
                plasma_gunsfx = pygame.mixer.music.load("sfx/plasma.mp3")
                pygame.mixer.music.play()

    def _ship_hit(self):
        #If ships left are more then 0:

        if self.stats.ships_left > 0:

            #If hit lose 1 live and, empty bullet and alien groups. Then create a new fleet then center the ship.

            self.stats.ships_left -= 1  

            self.sb.prep_ships()  #Decrement ships left and update scoreboard

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

            #Pause
            sleep(0.5)

        else:
            self.game_active = False        


    def sfx_click(self, event):
        num = random.randint(1,25)
        if num == 8:
            fartsfx = pygame.mixer.music.load("sfx/fart-with-reverb.mp3")
            pygame.mixer.music.play()
            print("reverb fart!!")
            
            #roachessfx = pygame.mixer.music.load("sfx/roaches.mp3")
            #pygame.mixer.music.load()

#------------------------------------------------------------------------------------------------------------------------------------------------------#

    def _create_fleet(self):
        #Create a fleet of aliens

        #Creating a alien
        alien = Alien(self)

        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height

        #OLD LOOP
        #Loop until there is no space for aliens: (while alien_x is more then screen_width - 2 * alien.width) 

        # *the -2 is to add space from the alien touching the edge of the screen, and spacing between aliens
        # *Y cord is bassicly X but opposite


        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            current_x = alien_width
            current_y += 2 * alien_height
                

    #Create 1 alien and set its X pos

    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position

        self.aliens.add(new_alien)


    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):

        #Drop the fleet and change fleet direction

        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

#------------------------------------------------------------------------------------------------------------------------------------------------------#

    def _update_bullets(self):
        
        #Functions

        self.bullets.update()

        self._check_bullet_alien_collisions()

        for bullet in self.bullets.copy():
            #if bullet reaches top simply remove from group
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            

    def _check_bullet_alien_collisions(self):
        #Check if bullets collided with groupcollide() if so remove

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)


        if collisions:
            for aliens in collisions.values():

            #add the current score by alien_points and multiply by the len(aliens), meaning how many aliens are hit by the bullet.

                self.stats.score += self.settings.alien_points * len(aliens)

            self.sb.check_high_scores()


        #If fleet is killed
        if not self.aliens:

            victory = pygame.mixer.music.load("sfx/output.mp3")
            pygame.mixer.music.play()

            sleep(11.5)
            
            self.stats.level += 1
            self.sb.prep_level()

            #If fleet is killed speed up game and recreate fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.speed_up()



    def _check_aliens_bottom(self):
        #If alien hits bottom of screen count as shiphit()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break


    def _update_aliens(self):

        #If alien is at edge check edges

        self._check_fleet_edges()
        self.aliens.update()

        #Check if ship collides with alien
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color) 

        #Update the screen/drawing bullets

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()

        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

 
#------------------------------------------------------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    ai = AlienInvasion()      
    ai.run_game()

#If an error is returned this line will start humiliating you, CREATING ANOTHER ERROR.
