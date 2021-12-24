import sys
from time import sleep

import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Main Game Class to manage game assets and behavior"""

    def __init__(self):
        """Initialise the game and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(self.settings.screen_dimensions)

        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.play_button = Button(self, "Play")

        pygame.display.set_caption("Alien Invasion!")

        # Create an instance to store the game stats
        # and create a scoreboard (sb)
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Set the background color
        self.bg_color = self.settings.screen_color

    def _update_bullets(self):
        """Update the positions of bullets and delete old bullets """
        self.bullets.update()
        for bullet in self.bullets:
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """Check for any bullets that have hit an alien"""
        # If so, get rid of the bullet and te alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Destroy the existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase the level
            self.stats.level += 1
            self.sb.prep_level()

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

    def _fire_bullet(self):
        """Create a new bullet instance and add it to the group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Create a new fleet of aliens"""
        # Create an alien and find out the number of aliens in the fleet
        # Spacing between each line is equal to the width of one alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        ship_height = self.ship.rect.height

        # calculation of available space on the screen.
        available_space_x = self.settings.screen_width - (2 * alien_width)
        no_of_aliens_x = available_space_x // (2 * alien_width)
        available_space_y = self.settings.screen_height - ((3 * alien_height) - ship_height)
        no_of_rows = available_space_y // (2 * alien_height)

        # Create the first row of aliens
        for row_number in range(no_of_rows):
            for alien_number in range(no_of_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in a row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_number * alien_width
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.y * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if alien has reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= (screen_rect.bottom - self.ship.height):
                # Treat this same as if the ship got hit
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """Respond appropriately if an alien has reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop Entire fleet and change the fleet direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.bottomright_ship()

            # Pause
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks 'Play'"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Initialize dynamic settings
            self.settings.initialize_dynamic_settings()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

            # Reset the game stats and activate the game
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining alien or bullets
            self.aliens.empty()
            self.bullets.empty()

    def _update_screen(self):
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Draw the score information
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_keydown_events(self, event):
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def run_game(self):
        """Start the main game loop"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()


if __name__ == "__main__":
    # Make a game instance then run it.
    ai = AlienInvasion()
    ai.run_game()
