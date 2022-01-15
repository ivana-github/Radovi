blue = (0, 0, 70)
width = 1100
height = 600

class Settings:
    # Class is storing all settings for the game.

    def __init__(self):
        self.screen_width = width
        self.screen_height = height
        self.background_color = blue

        self.astronaut_life_limit = 3
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # Settings that changes throughout the game.
        self.astronaut_speed = 2
        self.meteor_speed = 1
        self.earth_speed = 1
        self.chance_to_appear = 0.005

    def increase_speed(self):
        self.astronaut_speed *= self.speedup_scale
        self.meteor_speed *= self.speedup_scale
        self.chance_to_appear *= self.speedup_scale
