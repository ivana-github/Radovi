import pygame
import random
from pygame.sprite import Sprite

meteor_image_selection = ['images/meteor1.png', 'images/meteor2.png']
meteor_scale_selection = [(30, 30), (35, 35), (40, 40)]


class Meteor(Sprite):

    def __init__(self, game_parameters):
        super().__init__()
        self.settings = game_parameters.settings

        # Load an image and scale it.
        self.image = pygame.transform.scale(pygame.image.load(random.choice(meteor_image_selection)),
                                            random.choice(meteor_scale_selection))

        # Create every new meteor somewhere at the top of the screen.
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(self.settings.screen_width)
        self.rect.y = -self.rect.height

    def update(self):
        # Move the meteor down the screen.
        self.rect.y += self.settings.meteor_speed
