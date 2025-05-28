"""
Menu version 1
This is the initial version of the menu screen.
"""


# imports
import pygame
import os
import sys

# LINES 10 TO 35 NOT NECESSARY FOR MAIN PROGRAM; HOWEVER THEY ARE NEEDED FOR RUNNING INDEPENDENTLY

# size constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()

# setting up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon_path = os.path.join("Assets", "game_icon.png")
game_icon = pygame.image.load(icon_path)
pygame.display.set_icon(game_icon)
pygame.display.set_caption("-- Menu --")

# colours
grey = (166, 166, 166)
white = (255, 255, 255)
black = (0, 0, 0)

# fonts
score_font_path = os.path.join("Fonts", "Pixelify_Sans", "PixelifySans-VariableFont_wght.ttf")
score_font = pygame.font.SysFont(os.path.abspath(score_font_path), 50)
msg_font_path = os.path.join("assets", "Press_Start_2P", "PressStart2P-Regular.ttf")
msg_font = pygame.font.SysFont(score_font_path, 75)
exit_font = pygame.font.SysFont("freesansbold.ttf", 100, bold=True)


class Button:

    def __init__(self, texture, x, y, width=350, height=105):
        self.width = width
        self.height = height
        self.x_pos = x
        self.y_pos = y
        self.button_list = ["start", "option", "credits", "quit"]
        self.texture_name = texture
        self.texture = None
        self.set_texture()

    def set_texture(self):
        if self.texture_name not in self.button_list:
            texture_path = os.path.join("Assets", "menu", f"{self.texture_name}.png")
        else:
            texture_path = os.path.join("Assets", "menu", f"{self.texture_name}_button.png")
        self.texture = pygame.image.load(texture_path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    def show(self):
        screen.blit(self.texture, (self.x_pos, self.y_pos))


class Start:

    def __init__(self):
        self.logo_button = Button("racing_logo", 25, 25, 750, 200)
        self.start_button = Button("start", 25, 325)
        self.options_button = Button("option", 425, 325)
        self.credits_button = Button("credits", 25, 475)
        self.quit_button = Button("quit", 425, 475)


def menu_screen():

    screen.fill(grey)

    menu = Start()

    menu.logo_button.show()
    menu.start_button.show()
    menu.options_button.show()
    menu.credits_button.show()
    menu.quit_button.show()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


# main routine
menu_screen()
