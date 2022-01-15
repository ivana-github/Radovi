import pygame
from pygame.sprite import Sprite

astronaut_image = 'images/astronaut.png'
astronaut_scale = (70, 70)


class Astronaut(Sprite):

    def __init__(self, game_parameters):
        super().__init__()
        self.screen = game_parameters.screen
        self.speed = game_parameters.settings.astronaut_speed
        self.screen_rect = game_parameters.screen.get_rect()

        # Load the image and scale it.
        self.image = pygame.transform.scale(pygame.image.load(astronaut_image), astronaut_scale)

        # Place the astronaut in the center.
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center

        # Flags
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

    def update(self):
        # Update the astronaut's position based on the flags movement.
        if self.moving_up and self.rect.top > 0:
            self.rect.y -= self.speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += self.speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.speed

    def center_astronaut(self):
        # Center the astronaut.
        self.rect.center = self.screen_rect.center

    def blitme(self):
        # Draw the astronaut.
        self.screen.blit(self.image, self.rect)
