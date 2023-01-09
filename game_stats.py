class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        
        # the statistics are set properly when the GameStats instance is first created
        self.reset_stats()

        # Start Alien Invasion in an inactive state.
        self.game_active =  False

        # High score should never be reset.
        # Because the high score should never be reset, we initialize high_score in __init__() rather than in reset_stats().
        self.high_score = 0
        
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit

        # To reset the score each time a new game starts, 
        # we initialize score in reset_stats() rather than __init__().
        self.score = 0

        # To reset the level at the start of each new game, initialize it in reset_stats()
        self.level = 1