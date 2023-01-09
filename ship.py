import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""

    # takes two parameters: the self reference and a reference to the current instance of the AlienInvasion class
    # This will give Ship access to all the game resources defined in AlienInvasion
    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()

        # we assign the screen to an attribute of Ship, so we can access it easily in all the methods in this class
        self.screen = ai_game.screen
        
        # 
        self.settings = ai_game.settings

        # we access the screen’s rect attribute and assign it to self.screen_rect 
        # Doing so allows us to place the ship in the correct location on the screen.
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        # Double slash because windows issue with file slash 
        self.image = pygame.image.load('images/ship.bmp')

        # When the image is loaded, we call get_rect() to access the ship surface’s rect attribute so we can later use it to place the ship.
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        # We’ll position the ship at the bottom center of the screen.
        #  To do so, make the value of self.rect.midbottom match the midbottom attribute of the screen’s rect
        self.rect.midbottom = self.screen_rect.midbottom
        
        # Movement flags
        # set it to False initially
        self.moving_right = False
        self.moving_left  = False
        
        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

    # which moves the ship right/left if the flag is True
    # method will be called through an instance of Ship, so it’s not considered a helper method.
    def update(self):
        """Update the ship's position based on the movement flag."""

        # Update the ship's x value, not the rect.

        # The code self.rect.right returns the x-coordinate of the right edge of the ship’s rect.
        # If this value is less than the value returned by self.screen 
        # rect.right, the ship hasn’t reached the right edge of the screen
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        # The same goes for the left edge: if the value of the left side of the rect is greater than 
        # zero, the ship hasn’t reached the left edge of the screen
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        # Update rect object from self.x.
        self.rect.x = self.x
    
    # We center the ship the same way we did in __init__(). After centering it, 
    # we reset the self.x attribute, which allows us to track the ship’s exact position.
    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    # we define the blitme() method, which draws the image to the
    # screen at the position specified by self.rect.
    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
