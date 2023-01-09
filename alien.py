import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect =self.image.get_rect()

        # Start each new alien near the top left of the screen.
        # We initially place each alien near the top-left corner of the screen; 
        # we add a space to the left of it that’s equal to the alien’s width and
        # a space above it equal to its height so it’s easy to see.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        # We’re mainly concerned with the aliens’ horizontal speed, 
        # so we’ll track the horizontal position of each alien precisely
        self.x = float(self.rect.x)

    # We can call the new method check_edges() on any alien to see 
    # whether it’s at the left or right edge
    # 
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()

        # The alien is at the right edge if the right attribute 
        # of its rect is greater than or equal to the right attribute of the screen’s rect. 
        # It’s at the left edge if its left value is less than or equal to 0 .
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    # We create a settings parameter in __init__() so 
    # we can access the alien’s speed in update().
    # Each time we update an alien’s position, we move it to the right by the amount stored in alien_speed.
    def update(self):
        """"Move the alien right or left."""

        # We track the alien’s exact position with the self.x attribute,
        # which can hold decimal values
        # to allow motion to the left or right by multiplying the alien’s speed by the value of fleet_direction
        # If fleet _direction is 1, the value of alien_speed will be added to the alien’s current position,
        # moving the alien to the right; if fleet_direction is −1, the value will be subtracted from the alien’s position,
        # moving the alien to the left.
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)

        # We then use the value of self.x to update
        # the position of the alien’s rect
        self.rect.x  = self.x

    
