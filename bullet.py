import pygame 
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to mange bullets fried from the ship."""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position. """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color 

        # Create a bullet rect at (0, 0) and then set correct position.
        # we create the bullet’s rect attribute 
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_hight)

        #we set the bullet’s midtop attribute to match the ship’s midtop attribute
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position  as a decimal value
        #we can make fine adjustments to the bullet’s speed
        self.y = float(self.rect.y) 
    
    def update(self):
        """Move the bullet up the screen."""

        # Update the decimal position of the bullet. 
        # When a bullet is fired, it moves up the screen, which corresponds to a decreasing y-coordinate
        # value. To update the position, we subtract the amount stored in settings.bullet_speed from self.y
        self.y -= self.settings.bullet_speed

        # Update the rect position.
        # use the value of self.y to set the value of self.rect.y
        self.rect.y = self.y 

    # The draw.rect() function fills the part of the screen defined by 
    # the bullet’s rect with the color stored in self.color
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
