import pygame

from Pong import button

pygame.init()

width, height = 700, 500
window = pygame.display.set_mode((width, height))

# Load Images
one_img = pygame.image.load("images/button_one.png").convert_alpha()
two_img = pygame.image.load("images/button_two.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()

# Create button instances
one_button = button.Button(196, 85, one_img, 1)
two_button = button.Button(196, 209, two_img, 1)
quit_button = button.Button(286, 333, quit_img, 1)
