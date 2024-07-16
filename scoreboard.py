import pygame.font

from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    def __init__(self, ai_game):

        self.ai_game = ai_game

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #Styling the scoreboard
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()

        self.prep_level()

        self.prep_ships()




    def prep_score(self):
        #Render the scoreboard

        #Rounding the number, note that the -1 means to round to nearest ten

        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}" #The :, is a format specifier, telling python to add commas to the numbers.


        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20 


    def prep_high_score(self):

        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"

        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        #Center high score
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        
        #Render the level text
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10   #Position level 10 pixels under score.

    def prep_ships(self):  
        self.ships = Group()
        
        #Run a loop for every ship the player has left.
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)



    def check_high_scores(self):
        #Check to see if a new high score exists

        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        #Draw the scoreboard

        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
            