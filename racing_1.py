"""
Car Racing Version 1
Importing and instantiating the pygame module
Creating the screen
Setting up constants for colours, fonts and sizes
"""


# imports
import pygame
import sys
import os


# size constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


pygame.init()

# setting up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon_path = os.path.join("Assets", "game_icon.png")
game_icon = pygame.image.load(icon_path)
pygame.display.set_icon(game_icon)
pygame.display.set_caption("Car Racing Game - by Nathan Yew")

# colours
grey = (166, 166, 166)
white = (255, 255, 255)
black = (0, 0, 0)

# fonts
score_font_path = os.path.join("Fonts", "Pixelify_Sans", "PixelifySans-VariableFont_wght.ttf")
score_font = pygame.font.SysFont(os.path.abspath(score_font_path), 50)
exit_font = pygame.font.SysFont("freesansbold.ttf", 100, bold=True)


# Main loop function
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update()


# main routine
main()
