import pygame
import random
from pygame.sprite import Sprite

earth_image = 'images/earth.png'
earth_scale = (250, 250)


class Earth(Sprite):

    def __init__(self, game_parameters):
        super().__init__()
        self.settings = game_parameters.settings
        self.screen = game_parameters.screen

        self.every_second = False

        # Load an image and scale it.
        self.image = pygame.transform.scale(pygame.image.load(earth_image),
                                            earth_scale)

        # Create every new earth somewhere at the top of the screen.
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(self.settings.screen_width)
        self.rect.y = -self.rect.height

    def update(self):
        # Move the earth down the screen.
        if self.every_second:
            self.rect.y += self.settings.earth_speed
            self.every_second = False
        if not self.every_second:
            self.every_second = True

    def blitme(self):
        # Draw the earth.
        self.screen.blit(self.image, self.rect)