import pygame.font # which lets Pygame render text to the screen

class Button:
    # The __init__() method takes the parameters self, the ai_game
    # object, and msg, which contains the button’s text 
    def __init__(self, ai_game, msg):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        # We set the button dimensions
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)

        # and then set button_color to color the button’s rect object bright green 
        # and set text_color to render the text in white.
        self.text_color = (255, 255, 255)

        # we prepare a font attribute for rendering text. The None argument tells Pygame 
        # to use the default font, and 48 specifies the size of the text.
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        # To center the button on the screen, we create a rect for the button x and 
        # set its center attribute to match that of the screen.
        self.rect = pygame.Rect(0, 0, self.width ,self.height)
        self.rect.center = self.screen_rect.center 

        # The button message needs to be prepped only once.
        # we call _prep_msg() to handle this rendering.
        self._prep_msg(msg)

    # helper method
    # The _prep_msg() method needs a self parameter and the text to be rendered as an image (msg).
    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        # The call to font.render() turns the text stored in msg into an image,
        # which we then store in self.msg_image
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)

        # we center the text image on the button by creating a rect from
        # the image and setting its center attribute to match that of the button.
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    

    def draw_button(self):
        """ Draw blank button and then draw message."""

        # We call screen.fill() to draw the rectangular portion of the button.
        self.screen.fill(self.button_color, self.rect)

        # we call screen.blit() to draw the text image to the screen, passing it 
        # an image and the rect object associated with the image.
        self.screen.blit(self.msg_image, self.msg_image_rect)