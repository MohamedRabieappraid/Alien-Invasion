import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """A class to report scoring information."""

    # we give __init__() the ai_game parameter so it can access the settings, screen, and stats objects,
    # which it will need to report the values we’re tracking.
    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats


        # Font settings for scoring information.
        # Then we set a text color 
        self.text_color = (30,30,30)
        # and instantiate a font object
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image.
        # To turn the text to be displayed into an image, we call prep_score() 
        self.prep_score()

        # The high score will be displayed separately from the score, 
        # so we need a new method, prep_high_score(), to prepare the high score image.
        self.prep_high_score()

        # To have Scoreboard display the current level, we call a new method, prep_level()
        self.prep_level()

        # We assign the game instance to an attribute, because we’ll need it to 
        # create some ships. We call prep_ships() after the call to prep_level().
        self.prep_ships()

    # To turn the text to be displayed into an image 
    def prep_score(self):
        """Turn the score into a rendered image."""

        # tells Python to round the value of stats.score to the nearest 10 and store it in rounded_score.
        rounded_score = round(self.stats.score, -1)

        # a string formatting directive tells Python to insert commas into numbers when converting a 
        # numerical value to a string: for example, to output 1,000,000 instead of 1000000.
        score_str ="{:,}".format(rounded_score)

        # we turn the numerical value stats.score into a string
        score_str = str(self.stats.score)

        # and then pass this string to render(), which creates the image.
        # To display the score clearly onscreen, we pass the screen’s background color and the text color to render().
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.

        # To make sure the score always lines up with the right side of the screen, we create a rect called score_rect
        self.score_rect = self.score_image.get_rect()

        # and set its right edge 20 pixels from the right edge of the screen
        self.score_rect.right = self.screen_rect.right-20

        # We then place the top edge 20 pixels down from the top of the screen y.
        self.score_rect.top = 20 
    
    # method to display the rendered score image
    # This method draws the score image onscreen at the location score_rect specifies.
    def show_score(self):
        """Draw scores, level, and ships to the screen."""

        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)

        # This new line draws the level image to the screen.
        self.screen.blit(self.level_image, self.level_rect)

        # To display the ships on the screen, we call draw() on the group, and Pygame draws each ship.
        self.ships.draw(self.screen)


    def prep_high_score(self):
        """Turn the high score into a rendered image."""

        # We round the high score to the nearest 10 and format it with commas.
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)

        # We then generate an image from the high score
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()

        # center the high score rect horizontally
        self.high_score_rect.centerx = self.screen_rect.centerx

        # and set its top attribute to match the top of the score image
        self.high_score_rect.top = self.score_rect.top

    # To check for high scores 
    # The method check_high_score() checks the current score against the 
    # high score. If the current score is greater, we update the value of high_score and call prep_high_score() to update the high score’s image.
    def check_high_score(self):
        """Check to see if there's a new high score."""

        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    # The prep_level() method creates an image from the value stored in stats.level
    def prep_level(self):
        """Turn the level into a rendered image."""

        level_str = str(self.stats.level)

        # The prep_level() method creates an image from the value stored in stats.level
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()

        # sets the image’s right attribute to match the score’s right attribute.
        self.level_rect.right = self.score_rect.right

        # It then sets the top attribute 10 pixels beneath the bottom of 
        # the score image to leave space between the score and the level.
        self.level_rect.top = self.score_rect.bottom + 10 

    # The prep_ships() method creates an empty group
    def prep_ships(self):
        """Show how many ships are left."""

        # self.ships, to hold the ship instances.
        self.ships = Group()

        # To fill this group, a loop runs once for every ship the player has left.
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)

            # Inside the loop, we create a new ship and set each ship’s x-coordinate value so the ships appear 
            # next to each other with a 10-pixel margin on the left side of the group of ships.
            ship.rect.x = 10 + ship_number * ship.rect.width

            # We set the y-coordinate value 10 pixels down from the top of the screen so the ships appear in 
            # the upper-left corner of the screen.
            ship.rect.y = 10

            # Then we add each new ship to the group ships y.
            self.ships.add(ship)
