import pygame.font

red = (255, 0, 0)
blue = (0, 0, 50)
yellow = (220, 220, 0)
white = (255, 255, 255)

font_size = 60
font_type = 'Calibri'
font_type_congrats = 'comicsansms'


class Button:

    def __init__(self, game_parameters, msg):
        self.screen = game_parameters.screen
        self.settings = game_parameters.settings

        self.width, self.height = self.settings.screen_width / 12, self.settings.screen_height / 12,
        self.button_color = red
        self.text_color = blue
        self.font = pygame.font.SysFont(font_type, font_size)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen.get_rect().center

        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.rect.topleft

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Congratulations:

    def __init__(self, game_parameters, msg):
        self.screen = game_parameters.screen
        self.settings = game_parameters.settings

        self.width, self.height = self.settings.screen_width / 3, self.settings.screen_height / 8,
        self.button_color = yellow
        self.text_color = white
        self.font = pygame.font.SysFont(font_type_congrats, font_size)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen.get_rect().center

        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.rect.topleft

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)



