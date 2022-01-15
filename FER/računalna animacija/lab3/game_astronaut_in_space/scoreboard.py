import pygame.font
from pygame.sprite import Group
from game_astronaut_in_space.astronaut import Astronaut

red = (255, 0, 0)
font_size = 48
font_type = 'Calibri'
astronaut_life_scale = (50, 50)

class Scoreboard:
    def __init__(self, game_parameters):
        self.game_parameters = game_parameters
        self.screen = game_parameters.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game_parameters.settings
        self.stats = game_parameters.stats

        self.text_color = red
        self.font = pygame.font.SysFont(font_type, font_size)

        self.prep_game_time()
        self.prep_level()
        self.prep_astronauts()

    def prep_game_time(self):
        round_game_time = self.stats.game_time // 1000
        time_string = f"Time {round_game_time // 60:02}:{round_game_time % 60:02}"

        self.game_time_image = self.font.render(time_string, True, self.text_color,
                                                self.settings.background_color)

        self.game_time_rect = self.game_time_image.get_rect()
        self.game_time_rect.right = self.screen_rect.right - 15
        self.game_time_rect.top = 15

    def prep_level(self):
        level_string = "Level " + str(self.stats.level)
        self.level_image = self.font.render(level_string, True, self.text_color, self.settings.background_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.game_time_rect.right
        self.level_rect.top = self.game_time_rect.bottom + 10

    def prep_astronauts(self):
        self.austronauts = Group()
        for monster_number in range(self.stats.life_left):
            astronaut = Astronaut(self.game_parameters)
            astronaut.image = pygame.transform.scale(astronaut.image, astronaut_life_scale)
            astronaut.rect.x = 5 + monster_number * astronaut.rect.width
            astronaut.rect.y = 10
            self.austronauts.add(astronaut)

    def show_time(self):
        # Draw the time, level, and astronauts.
        self.screen.blit(self.game_time_image, self.game_time_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.austronauts.draw(self.screen)
