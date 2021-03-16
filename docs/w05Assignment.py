#---------------------------------------------------
# This program implements a simplistic version of the
# classic Pong arcade game.
#
# Written by Anastasia Lysenko, 5/27/2020.
#---------------------------------------------------

import arcade
import random
from random import randint

# These are Global constants to use throughout the game
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
BALL_RADIUS = 10

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 50
MOVE_AMOUNT = 4

SCORE_HIT = 1
SCORE_MISS = 5

class Point:
    '''Point class to represent a point in the coordinate system.'''
    def __init__(self):
        '''Initializes Point object with default values.'''
        self.x = 0.0    # x coordinate location on our window
        self.y = 0.0    # y coordinate location on our window

class Velocity:
    '''Velocity class to represent a velocity in the coordinate system.'''
    def __init__(self):
        '''Initializes Velocity object with default values.'''
        self.dx = 0.0   # how fast it changes in x direction
        self.dy = 0.0   # how fast it changes in y direction
 
class Ball:
    '''Ball class to make a ball appear and move in the window.'''
    def __init__(self):
        '''Initializes Ball object along the left edge of the screen, and with a random velocity.'''
        self.center = Point() 
        self.center.x = BALL_RADIUS  # make sure half of the ball is not outside the screen
        self.center.y = randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS) # random y coordinate, but make sure
        # the ball is within the screen
        self.velocity = Velocity()
        self.velocity.dx = randint(MOVE_AMOUNT, 2*MOVE_AMOUNT)  
        self.velocity.dy = randint(MOVE_AMOUNT-2, MOVE_AMOUNT-1)  # make sure not the same speed as dx or paddle
        # would not need to move to catch the ball

    def draw(self):
        '''Draws a circle (ball) with a center at: x = self.center.x, y = self.center.y.'''
        arcade.draw_circle_filled(self.center.x, self.center.y, BALL_RADIUS, arcade.color.BURGUNDY)
    
    def advance(self):
        '''Advances the circle based on velocity for 1 frame.'''
        self.center.x +=self.velocity.dx
        self.center.y +=self.velocity.dy

    def bounce_horizontal(self):
        '''Inverts to switch horizontal direction of the ball if the ball hits the wall to the left.'''
        self.velocity.dx *= -1
    
    def bounce_vertical(self):
        '''Inverts to switch vertical direction of the ball if the ball hits the wall above or below.'''
        self.velocity.dy *= -1

    def restart(self):
        '''Resets ball's position after the ball is lost.'''
        self.center.x = 0.0
        self.center.y = randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)
        self.velocity.dx = randint(MOVE_AMOUNT, 2*MOVE_AMOUNT) # positive, want to move right
        self.velocity.dy = randint(MOVE_AMOUNT-2, MOVE_AMOUNT-1) 
 

 
class Paddle:
    '''Paddle class to make a paddle appear and move in the window.'''
    def __init__(self):
        '''Initializes Paddle object.'''
        self.center = Point()
        self.center.x = SCREEN_WIDTH-PADDLE_WIDTH  # make sure paddle is does not dissappear off the window
        self.center.y = SCREEN_HEIGHT / 2  
        
    def draw(self):
        '''Creates a black rectangle (paddle) with a center at: x = self.center.x, y = self.center.y.'''
        arcade.draw_rectangle_filled(self.center.x, self.center.y,PADDLE_WIDTH, PADDLE_HEIGHT, 
                                     arcade.color.BLACK)
    
    def move_up(self):
        '''Moves the paddle up.'''
        if self.center.y < SCREEN_HEIGHT - PADDLE_HEIGHT / 2: # make sure the paddle stops moving up as 
            # soon as it goes off the window
            self.center.y += MOVE_AMOUNT
        
    
    def move_down(self):
        '''Moves the paddle down.'''
        if self.center.y > PADDLE_HEIGHT / 2: # make sure the paddle stops moving down as soon as
            # it goes off the window
            self.center.y -= MOVE_AMOUNT


class Pong(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Point
        Velocity
        Ball
        Paddle
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class,
    but should not have to if you don't want to.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.ball = Ball()
        self.paddle = Paddle()
        self.score = 0

        # These are used to see if the user is
        # holding down the arrow keys
        self.holding_left = False
        self.holding_right = False

        arcade.set_background_color(arcade.color.BRITISH_RACING_GREEN)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsiblity of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.ball.draw()
        self.paddle.draw()

        self.draw_score()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.WHITE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """

        # Move the ball forward one element in time
        self.ball.advance()

        # Check to see if keys are being held, and then
        # take appropriate action
        self.check_keys()

        # check for ball at important places
        self.check_miss()
        self.check_hit()
        self.check_bounce()

    def check_hit(self):
        """
        Checks to see if the ball has hit the paddle
        and if so, calls its bounce method.
        :return:
        """
        too_close_x = (PADDLE_WIDTH / 2) + BALL_RADIUS
        too_close_y = (PADDLE_HEIGHT / 2) + BALL_RADIUS

        if (abs(self.ball.center.x - self.paddle.center.x) < too_close_x and
                    abs(self.ball.center.y - self.paddle.center.y) < too_close_y and
                    self.ball.velocity.dx > 0):
            # we are too close and moving right, this is a hit!
            self.ball.bounce_horizontal()
            self.score += SCORE_HIT

    def check_miss(self):
        """
        Checks to see if the ball went past the paddle
        and if so, restarts it.
        """
        if self.ball.center.x > SCREEN_WIDTH:
            # We missed!
            self.score -= SCORE_MISS
            self.ball.restart()

    def check_bounce(self):
        """
        Checks to see if the ball has hit the borders
        of the screen and if so, calls its bounce methods.
        """
        if self.ball.center.x < BALL_RADIUS and self.ball.velocity.dx < 0:
            self.ball.bounce_horizontal()

        if self.ball.center.y < BALL_RADIUS and self.ball.velocity.dy < 0:
            self.ball.bounce_vertical()

        if self.ball.center.y > SCREEN_HEIGHT - BALL_RADIUS and self.ball.velocity.dy > 0:
            self.ball.bounce_vertical()

    def check_keys(self):
        """
        Checks to see if the user is holding down an
        arrow key, and if so, takes appropriate action.
        """
        if self.holding_left:
            self.paddle.move_down()

        if self.holding_right:
            self.paddle.move_up()

    def on_key_press(self, key, key_modifiers):
        """
        Called when a key is pressed. Sets the state of
        holding an arrow key.
        :param key: The key that was pressed
        :param key_modifiers: Things like shift, ctrl, etc
        """
        if key == arcade.key.LEFT or key == arcade.key.DOWN:
            self.holding_left = True

        if key == arcade.key.RIGHT or key == arcade.key.UP:
            self.holding_right = True

    def on_key_release(self, key, key_modifiers):
        """
        Called when a key is released. Sets the state of
        the arrow key as being not held anymore.
        :param key: The key that was pressed
        :param key_modifiers: Things like shift, ctrl, etc
        """
        if key == arcade.key.LEFT or key == arcade.key.DOWN:
            self.holding_left = False

        if key == arcade.key.RIGHT or key == arcade.key.UP:
            self.holding_right = False

# Creates the game and starts it going
window = Pong(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()