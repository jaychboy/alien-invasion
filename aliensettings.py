class Settings:

    def __init__(self):
        #Display
        self.screen_width = 1400
        self.screen_height = 900
        self.bg_color = (230, 230, 230)

        #Ship
        self.ship_speed = 3
        self.ship_limit = 3

        #Alien
        self.alien_speed = 1.4
        self.fleet_drop_speed = 10.5
        self.fleet_direction = 1

        #Bullet
        self.bullet_width = 4 #1500 is gonna kill a whole row. 4
        self.bullet_height = 21  #4000 with no collision with aliens = Laser. 25

        #Bullet -styling
        self.bullet_color = (215, 1, 0)
        self.bullet_speed = 5
        self.bullets_allowed = 16

        #Other
        self.speedup_scale = 1.2

        self.score_scale = 1.5

        self.initialize_dynamic_settings()

        
    def speed_up(self):
        #Speed up the game every time a fleet is killed.

        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed = self.speedup_scale
        
        #Each fleet that is killed multiply the amount of points that you get per alien for the next fleet.

        self.alien_points = int(self.alien_points * self.score_scale)

        print(self.alien_points)


    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 5
        self.alien_speed = 1.0

        #1 for right, -1 for left
        self.fleet_direction = 1

        self.alien_points = 50 #Amount earned for each alien killed.
        