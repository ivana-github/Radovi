class GameStats:
    # Tracking statistics.

    def __init__(self, game_parameters):
        self.settings = game_parameters.settings
        self.reset_stats()

        self.game_active = False

    def reset_stats(self):
        # Initialize statistics that can change during the game.
        self.life_left = self.settings.astronaut_life_limit
        self.level = 1
        self.game_time = 0
