import pygame.font

class Button:

    def __init__(self, ai_game, msg):
        
        #Init button 
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        #Styling
        self.width, self.height = 300, 75
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
    

        #Get button rect and center it: make a rect then center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #Prep button message/render text
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        #Render the text and center it

        #Set some attributes
        self.msg_image = self.font.render(msg, True, self.text_color, 
                self.button_color)

        #Center the button
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #Draw button then enter in message

        #Draw and fill with color
        self.screen.fill(self.button_color, self.rect)
        
        #Draw text
        self.screen.blit(self.msg_image, self.msg_image_rect)

