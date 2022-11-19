# import the pygame module
import pygame
import sys
import os

 
# import pygame.locals for easier
# access to key coordinates
from pygame.locals import *
 
# Define our square object and call super to
# give it all the properties and methods of pygame.sprite.Sprite
# Define the class for our square objects
class Square(pygame.sprite.Sprite):
    def __init__(self):
        super(Square, self).__init__()
         
        # Define the dimension of the surface
        # Here we are making squares of side 25px
        self.surf = pygame.Surface((25, 25))
         
        # Define the color of the surface using RGB color coding.
        self.surf.fill((0, 200, 255))
        self.rect = self.surf.get_rect()
 
# initialize pygame
pygame.init()

#Start timing
clock = pygame.time.Clock()

# Load the background image here.
bg = pygame.image.load(os.path.join("./", "Pygame/city_scape.png"))

pygame.mouse.set_visible(0)

pygame.display.set_caption('Flying saucer game')

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
 
# assigning values to X and Y variable
X = 400
Y = 400
 
# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((X, Y))
 
# set the pygame window name
pygame.display.set_caption('Show Text')
 
# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)
 
# create a text surface object,
# on which text is drawn on it.
text = font.render('Space Game', True, green, blue)
 
# create a rectangular object for the
# text surface object
textRect = text.get_rect()
 
# set the center of the rectangular object.
textRect.center = (X // 2, Y // 2)
 
# Define the dimensions of screen object
screen = pygame.display.set_mode((800, 280))
 
# instantiate all square objects
square1 = Square()
square2 = Square()
square3 = Square()
square4 = Square()
 
# Variable to keep our game loop running
gameOn = True
 
# Our game loop
while gameOn:
    # completely fill the surface object
    # with white color
    display_surface.fill(white)
    # Start the
    clock.tick(60)

    screen.blit(bg, (0, 0))
 
    # copying the text surface object
    # to the display surface object
    # at the center coordinate.
    display_surface.blit(text, textRect)
    # for loop through the event queue
    for event in pygame.event.get():
         
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
             
            # If the Backspace key has been pressed set
            # running to false to exit the main loop
            if event.key == K_BACKSPACE:
                gameOn = False
                 
        # Check for QUIT event
        elif event.type == QUIT:
            gameOn = False
 
    # Define where the squares will appear on the screen
    # Use blit to draw them on the screen surface
    screen.blit(square1.surf, (40, 40))
    screen.blit(square2.surf, (40, 250))
    screen.blit(square3.surf, (750, 40))
    screen.blit(square4.surf, (750, 250))
 
    # Update the display using flip
    pygame.display.flip()



 
# infinite loop
while True:
 

 
    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for event in pygame.event.get():
 
        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:
 
            # deactivates the pygame library
            pygame.quit()
 
            # quit the program.
            quit()
 
        # Draws the surface object to the screen.
        pygame.display.update()