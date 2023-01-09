import sys 
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game , and create the game resources."""
        pygame.init()

        # create an instance of Settings and assign it to self.settings
        self.settings = Settings()

        #  we use the screen_width and screen_height attributes of self.settings
        # we set the full screen mode 
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("ALien Invasion")
        
        # Create an instance to store game statistics.
        
        self.stats = GameStats(self)

        # and create an instance for scoreboard.
        self.sb = Scoreboard(self)

        # make an instance of Ship after the screen has been created The self argument here refers to the current instance of AlienInvasion
        # This is the parameter that gives Ship access to the game’s resources
        # such as the screen object. We assign this Ship instance to self.ship.
        self.ship = Ship(self)

        # This group will be an instance of the pygame.sprite.Group class,
        # which behaves like a list with some extra 
        # functionality that’s helpful when building games
        self.bullets = pygame.sprite.Group()

        self.aliens  = pygame.sprite.Group()

        self._create_fleet()

        # Make the Play button.
        # This code creates an instance of Button with the label Play 
        # but it doesn’t draw the button to the screen.
        self.play_button = Button(self, "Play")



    # It’s easy to see that we’re looking for new events and updating the screen on each pass through the loop.
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events by using _check_events method and _update_screen and ship.update 
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
   
    # helper method
    # Watch for keyboard and mouse events.
    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():

            # when the player clicks the game window’s close button
            if event.type == pygame.QUIT:

                # and we call sys.exit() to exit the game
                sys.exit()

            # Pygame detects a MOUSEBUTTONDOWN event when the player clicks anywhere on the screen  
            # but we want to restrict our game to respond to mouse clicks only on the Play button.
            elif event.type == pygame.MOUSEBUTTONDOWN:

                #  To accomplish this, we use pygame.mouse.get_pos(), which returns a tuple containing 
                #  the mouse cursor’s x- and y-coordinates when the mouse button is clicked.
                mouse_pos = pygame.mouse.get_pos()

                # We send these values to the new method _check_play_button() w.
                self._check_play_button(mouse_pos)
            
    
            # respond when Pygame detects a KEYDOWN event
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
               
            # we add a new elif block, which responds to KEYUP events. 
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    # helper method
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""

        # The flag button_clicked stores a True or False value
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        # the game will restart only if Play is clicked and the game is not currently active.
        if button_clicked and not self.stats.game_active:

            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            # we reset the game statistics, which gives the player three new ships.
            self.stats.reset_stats()

            # If so, we set game_active to True, and the game begins!
            # Then we set game_active to True so the game will begin as soon as 
            # the code in this function finishes running.
            self.stats.game_active =True 

            # We call prep_score() after resetting the game stats when starting a new game.
            #  This preps the scoreboard with a 0 score.
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            # Get rid of any remaining aliens and bullets.
            # We empty the aliens and bullets groups
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            # then create a new fleet and center the ship. 
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            # Passing False to set_visible() tells Pygame to hide the cursor 
            # when the mouse is over the game window.
            pygame.mouse.set_visible(False)

    # helper method
    def _check_keydown_events(self, event):
        """Respond to keypresses."""

        # We check whether the key pressed, event.key, is the right arrow key
        # The right arrow key is represented by pygame.K_RIGHT
        if event.key == pygame.K_RIGHT:

            # we modify how the game responds when the player presses the right arrow key
            # instead of changing the ship’s position directly, we merely set moving_right to True
            self.ship.moving_right = True

        # We check whether the key pressed, event.key, is the left arrow key
        # The right arrow key is represented by pygame.K_LEFT
        elif event.key == pygame.K_LEFT:

            # we modify how the game responds when the player presses the left arrow key
            # instead of changing the ship’s position directly, we merely set moving_left to True
            self.ship.moving_left = True   
         
        # ends the game when the player presses Q
        elif event.key ==  pygame.K_q:
            sys.exit()

        # we call _fire_bullet() when the spacebar is pressed
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        
    # helper method
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        # When the player releases the right arrow key (K_RIGHT),
        # we set moving_right to False.
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right=False
                    
        # When the player releases the left arrow key (K_LEFT),
        # we set moving_LEFT to False.
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left=False
    

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            # we make an instance of Bullet and call it new_bullet
            new_bullet = Bullet(self)
            # We then add it to the group bullets using the add() method x.
            # The add() method is similar to append(), but it’s a method 
            # that’s written specifically for Pygame groups.
            self.bullets.add(new_bullet)


    # helper method
    # We moved the code that draws the background and the ship and flips the screen to _update_screen().                
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""

        # Redraw the screen during each pass through the loop.
        # we use self.settings to access the background color when filling the screen
        self.screen.fill(self.settings.bg_color)

        # we draw the ship on the screen by calling ship.blitme(), so the ship appears on top of the background
        self.ship.blitme()
        
        # The bullets.sprites() method returns a list of all sprites in the group bullets. 
        # To draw all fired bullets to the screen, we loop through the sprites in bullets 
        # and call draw_bullet() on each one
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        # To make the Play button visible above all other elements on the screen, 
        # we draw it after all the other elements have been drawn but before flipping to a new screen.
        # We include it in an if block, so the button only appears when the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()


    # helper method
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # the group automatically calls update() for each sprite in the group.
        # The line self.bullets.update() calls bullet.update()
        # for each bullet we place in the group bullets.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        # We use the copy() method to set up the for loop ,
        # which enables us to modify bullets inside the loop.
        for bullet in self.bullets.copy():
            # We check each bullet to see whether 
            # it has disappeared off the top of the screen 
            if bullet.rect.bottom <= 0:
                # If it has, we remove it from bullets 
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    # helper method
    # look for collisions between bullets and aliens, and to respond appropriately
    # if the entire fleet has been destroyed
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        
        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        # To make a high-powered bullet that can travel to the top of the screen, destroying every alien in its path,
        # you could set the first Boolean argument to False and keep the second Boolean argument set to True. 
        # The aliens hit would disappear, but all bullets would stay active until they disappeared off the top of the screen.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # When a bullet hits an alien, Pygame returns a collisions dictionary. 
        # We check whether the dictionary exists, and if it does, the alien’s value is 
        # added to the score. We then call prep_score() to create a new image for the updated score.
        if collisions:
            # If the collisions dictionary has been defined, we loop through all values in the dictionary.
            for aliens in collisions.values():
                # Remember that each value is a list of aliens hit by a single bullet. 
                # We multiply the value of each alien by the number of aliens in each list and add this amount to the current score.
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            # We call check_high_score() when the collisions dictionary is present, and 
            # we do so after updating the score for all the aliens that have been hit.
            self.sb.check_high_score()

        # We’ll perform this check at the end of _update_bullets(), 
        # because that’s where individual aliens are destroyed.
        # we check whether the aliens group is empty. An empty group evaluates to False, 
        # so this is a simple way to check whether the group is empty.
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            # If it is, we get rid of any existing bullets by using the empty() method,
            # which removes all the remaining sprites from a group
            self.bullets.empty()
            # We also call _create_fleet(), which fills the screen with aliens again.
            self._create_fleet() 
            # Changing the values of the speed settings ship_speed, alien_speed, 
            # and bullet_speed is enough to speed up the entire game! 
            self.settings.increase_speed()
            #Increase level.
            self.stats.level += 1
            self.sb.prep_level()
    # helper method
    def _create_fleet(self):
        """Create the fleet of aliens."""

        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        # We need to know the alien’s width and height to place aliens, so we create an alien
        # before we perform calculations. This alien won’t be part of the fleet, so don’t add it to the group aliens.
        alien = Alien(self)

        # we use the attribute size, which contains a tuple with the width and height of a rect object.
        alien_width, alien_height = alien.rect.size

        # we get the alien’s width from its rect attribute and store this value in alien_width so
        # we don’t have to keep working through the rect attribute.
        alien_width = alien.rect.width

        # we calculate the horizontal space available for aliens and 
        # the number of aliens that can fit into that space.
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)


        # Determine the number of rows of aliens that fit on the screen.
        # To calculate the number of rows we can fit on the screen, we write our available_space_y 
        # calculation right after the calculation for available_space_x
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)


        # Create the full fleet of aliens.
        # To create multiple rows, we use two nested loops: one outer and one inner loop
        for row_number in range(number_rows):
            # Create the first row of aliens.
            # we set up a loop that counts from 0 to the number of aliens we need to make
            for alien_number in range(number_aliens_x):
                # Create an alien and place it in the row.
                self._create_alien(alien_number,row_number)
            

    # helper method 
    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)

        # i don't use this varable alien_height in this function and this is weird (mohamed rabie says that)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number

        # In the main body of the loop, we create a new alien and then 
        # set its x-coordinate value to place it in the row
        alien.rect.x = alien.x 

        # we change an alien’s y-coordinate value when it’s not in the first row x 
        # by starting with one alien’s height to create empty space at the top of the screen
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
    
    # helper method
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            # In _change_fleet_direction(), we loop through all the aliens and
            # drop each one using the setting fleet_drop_speed
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1



    # helper method
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        
        # we loop through the fleet and call check_edges() on each alien
        for alien in self.aliens.sprites():
            # If check_edges() returns True, we know an alien is at an edge and the whole fleet needs to change direction; 
            # so we call _change_fleet_direction() and break out of the loop
            if alien.check_edges():
                self._change_fleet_direction()
                break
        

    

    # helper method
    # The new method _ship_hit() coordinates the response when an alien hits a ship.
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            # Inside _ship_hit(), the number of ships left is reduced by 1
            self.stats.ships_left -=1
            self.sb.prep_ships()
            # Get rid of any remaining aliens and bullets.
            # after which we empty the groups aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            # we create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            # Then we add a pause after the updates have been made to all the game elements but 
            # before any changes have been drawn to the screen,
            #  so the player can see that their ship has been hit
            sleep(0.5)
        else :
            self.stats.game_active = False

            # We make the cursor visible again as soon as the game becomes inactive,
            # which happens in _ship_hit().
            pygame.mouse.set_visible(True)

    # helper method
    # The method _check_aliens_bottom() checks whether any aliens have reached the bottom of the screen
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            # An alien reaches the bottom when its rect.bottom value is
            # greater than or equal to the screen’s rect.bottom attribute
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                # If an alien reaches the bottom, we call _ship_hit(). 
                # If one alien hits the bottom
                self._ship_hit()
                # there’s no need to check the rest, so we break out of the loop after calling _ship_hit().
                break


    # helper method
    # We use the update() method on the aliens group, 
    # which calls each alien’s update() method.
    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
        then update the positions of all aliens in the fleet.
        """
        # calling _check_fleet_edges() before updating each alien’s position.
        self._check_fleet_edges()
        self.aliens.update()
        
        # Look for alien-ships collisions.
        # If no collisions occur, spritecollideany() returns None and the if block at won’t execute.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):

            # If it finds an alien that has collided with the ship, it returns that alien and 
            # the if block executes: it prints Ship hit!!!
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        # We call _check_aliens_bottom() after updating the positions of 
        # all the aliens and after looking for alien and ship collisions
        self._check_aliens_bottom()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()