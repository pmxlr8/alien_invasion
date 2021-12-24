import pygame.font


class Settings:
    """A class to store all the game's settings"""

    def __init__(self):
        """Initialize the game's static settings"""

        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.screen_dimensions = (self.screen_width, self.screen_height)
        self.screen_color = (230, 230, 230)

        # Ship Settings
        self.ship_limit = 2  # Set this one lower than the number of ships you want
        # Because ships_left <= 0 will be checked after the last round of game has started

        # Bullet Settings
        self.bullet_width = 6
        self.bullet_height = 20
        self.bullet_color = (230, 60, 60)
        self.bullets_allowed = 10

        # Alien settings
        self.fleet_drop_speed = 10

        # Score settings
        #  How quickly the alien point value increases
        self.score_scale = 1.5
        self.alien_points = 50 / self.score_scale  # It will be multiplied by speedup_scale on starting also

        # Button settings
        self.button_width = 200
        self.button_height = 50
        self.button_color = (0, 255, 0)

        # Font Settings
        self.text_color = (255, 255, 255)
        self.score_text_color = (25, 25, 25)
        self.button_font = pygame.font.SysFont("Courier New", 50)
        self.score_font = pygame.font.SysFont("Courier New", 30)

        # How fast the game speeds up
        self.speedup_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize dynamic settings : settings that change throughout the game"""
        # It will be multiplied by speedup_scale on starting also
        self.ship_speed = 5 / self.speedup_scale
        self.bullet_speed = 5 / self.speedup_scale
        self.alien_speed = 1.0 / self.speedup_scale

        # fleet direction of 1 indicates right while -1 represents left and 0 represents rest
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase the speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)