import sys
import time

import pygame
import random
from game_astronaut_in_space.settings import Settings
from game_astronaut_in_space.astronaut import Astronaut
from game_astronaut_in_space.meteor import Meteor
from game_astronaut_in_space.game_stats import GameStats
from game_astronaut_in_space.button import Button, Congratulations
from game_astronaut_in_space.scoreboard import Scoreboard
from game_astronaut_in_space.earth import Earth


class Astronaut_in_space:

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Astronaut lost in space")

        # Create an instance to store game statistics, and create a scoreboard.
        self.stats = GameStats(self)
        self.score_board = Scoreboard(self)

        self.astronaut = Astronaut(self)
        self.meteors = pygame.sprite.Group()
        self.earth = pygame.sprite.Group()

        self.play_button = Button(self, "Start")
        self.earth_created = False
        self.seconds_til_earth = random.randint(1, 6) * 10000

    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self._create_meteors()
                self.astronaut.update()
                self._update_meteors()
                self._check_timer()
                if self.stats.game_time > self.seconds_til_earth:
                    if not self.earth_created:
                        self._create_earth()
                        self.earth_created = True
                    self._update_earth()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings and get start_time.
            self.start_game_time = pygame.time.get_ticks()
            self.stats.last_time = self.start_game_time
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.score_board.prep_game_time()
            self.score_board.prep_level()
            self.score_board.prep_astronauts()

            # Get rid of any remaining stars.
            self.meteors.empty()

            # Center the astronaut.
            self.astronaut.center_astronaut()

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_UP:
            self.astronaut.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.astronaut.moving_down = True
        elif event.key == pygame.K_RIGHT:
            self.astronaut.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.astronaut.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_UP:
            self.astronaut.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.astronaut.moving_down = False
        elif event.key == pygame.K_RIGHT:
            self.astronaut.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.astronaut.moving_left = False

    def _update_meteors(self):
        """Update position of stars and get rid of fallen stars."""
        # Update stars` positions.
        self.meteors.update()

        if pygame.sprite.spritecollideany(self.astronaut, self.meteors):
            self._astronaut_hit()

        # Get rid of stars that have disappeared.
        for star in self.meteors.copy():
            if star.rect.top >= self.settings.screen_height:
                self.meteors.remove(star)

    def _update_earth(self):
        """Update position of earth."""
        # Update earth` positions.
        self.earth.update()

        if pygame.sprite.spritecollideany(self.astronaut, self.earth):
            self._astronaut_hit_earth()

    def _check_timer(self):
        """Track game time and increase speed after each 10 sec"""
        ticks = pygame.time.get_ticks()
        self.stats.game_time = (ticks - self.start_game_time)

        # Increase speed and level.
        if self.stats.game_time - self.stats.last_time > 10000:
            self.stats.last_time = self.stats.game_time
            self.settings.increase_speed()
            self.stats.level += 1

        # Show time and level.
        self.score_board.prep_game_time()
        self.score_board.prep_level()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.background_color)
        self.astronaut.blitme()
        self.meteors.draw(self.screen)
        if self.stats.game_time > 1000:
            self.earth.draw(self.screen)


        # Draw the time information.
        self.score_board.show_time()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _create_meteors(self):
        self.meteors.add(Meteor(self)) if (random.random() < self.settings.chance_to_appear) else 1

    def _astronaut_hit(self):
        if self.stats.life_left > 0:
            # Decrease astronaut life, update scoreboard, remove meteors and center the monster.
            self.stats.life_left -= 1
            self.meteors.empty()
            self.score_board.prep_astronauts()
            self.astronaut.center_astronaut()
        else:
            self.stats.game_active = False

    def _astronaut_hit_earth(self):
        self.stats.game_active = False

        congrats = Congratulations(self, "Congradulations")
        congrats.draw_button()

        pygame.display.flip()

        time.sleep(5)
        self.earth_created = False
        for e in self.earth.copy():
            self.earth.remove(e)

    def _create_earth(self):
        self.earth.add(Earth(self))


if __name__ == '__main__':
    # Make a game instance, and run the game.
    fs = Astronaut_in_space()
    fs.run_game()
