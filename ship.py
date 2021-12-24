import pygame
from pygame.sprite import  Sprite


class Ship(Sprite):
    """A ship class to store all the details related to the ship"""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        super().__init__()

        self.settings = ai_game.settings

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load("ship.bmp")
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Start each ship from the bottom center of the screen
        self.rect.bottomright = self.screen_rect.bottomright

        # Movement Flags
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the ship's position based on movement flag"""
        if self.moving_left and (self.rect.x >= 0):
            self.rect.x -= self.settings.ship_speed
        elif self.moving_right and (self.rect.x <= (self.settings.screen_width-self.width)):
            self.rect.x += self.settings.ship_speed

    def bottomright_ship(self):
        """Bottomright the ship on the screen"""
        self.rect.bottomright = self.screen_rect.bottomright
        self.x = float(self.rect.x)