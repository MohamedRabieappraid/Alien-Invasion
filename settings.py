class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        # Ship settings 
        # We set the initial value of ship_speed to 1.5. When the ship moves 
        # now, its position is adjusted by 1.5 pixels rather than 1 pixel on each pass through the loop.
        self.ship_speed = 1.5
        self.ship_limit = 3
        
        # Bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_hight = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 1.0

        # The setting fleet_drop_speed controls how quickly the fleet drops down the screen each time 
        # an alien reaches either edge. It’s helpful to separate
        # this speed from the aliens’ horizontal speed so you can adjust the two speeds independently.
        self.fleet_drop_speed = 5 # 10

        # How quickly the game speeds up
        # we add a speedup_scale setting to control how quickly the game speeds up
        # If the game becomes too difficult too quickly, decrease the value of settings.speedup_scale. 
        # Or if the game isn’t challenging enough, increase the value slightly.
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        # We define a rate at which points increase, which we call score_scale.
        self.score_scale = 1.5

        # we call the initialize_dynamic_settings() method to initialize 
        # the values for attributes that need to change throughout the game.
        self.initialize_dynamic_settings()

        # fleet_direction of 1 represents right; -1 represents left.
        # because we have only two directions to deal with, let’s use 
        # the values 1 and −1, and switch between them each time the fleet changes direction.
        #####################################################################################################
        # (Using numbers also makes sense because moving right involves adding to each alien’s              #
        # x-coordinate value, and moving left involves subtracting from each alien’s x-coordinate value.)   #
        #####################################################################################################

        self.fleet_direction = 1 

    # This method sets the initial values for the ship, bullet, and alien speeds.
    # We’ll increase these speeds as the player progresses in the game and reset them each time the player starts a new game.
    # We include fleet_direction in this method so the aliens always move right at the beginning of a new game.
    # We don’t need to increase the value of fleet_drop_speed,because when the aliens move faster across the screen, they’ll also come down the screen faster.
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        # We’ll increase each alien’s point value as the game progresses. To make sure this point value is reset each time a new game starts, 
        # we set the value in initialize_dynamic_settings().
        self.alien_points = 50

    # To increase the speed of these game elements, 
    # we multiply each speed setting by the value of speedup_scale.
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        # when we increase the game’s speed, we also increase the point value of each hit.
        # We use the int() function to increase the point value by whole integers.
        self.alien_points = int(self.alien_points * self.score_scale)
        