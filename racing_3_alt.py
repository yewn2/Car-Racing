"""
Car Racing Version 3 (alternate version)
Creating the Car class
Implementing a player object into the game with controllable movement (WASD)
This version is my trialled version, in which I attempted to implement a different movement
style for the Car object.
"""

# imports
import pygame
import random
import math
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
msg_font_path = os.path.join("assets", "Press_Start_2P", "PressStart2P-Regular.ttf")
msg_font = pygame.font.SysFont(score_font_path, 75)
exit_font = pygame.font.SysFont("freesansbold.ttf", 100, bold=True)


# Background class
class Background:
    def __init__(self, y):
        self.texture = None
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.y_pos = y
        self.set_texture()
        self.show()

    # Making background self scroll
    def update_bg(self, by):
        self.y_pos -= by
        if self.y_pos >= SCREEN_HEIGHT:
            self.y_pos = -SCREEN_HEIGHT

    # Displaying background
    def show(self):
        screen.blit(self.texture, (0, self.y_pos))

    # Loading background and transforming to appropriate size
    def set_texture(self):
        path = os.path.join("Assets", "road.png")
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))


# Car class
class Car:

    def __init__(self, player_state):
        if player_state == "yes":
            self.player = True
        elif player_state == "no":
            self.player = False
            self.texture = None
        self.width = 100
        self.height = 200
        self.x_pos = 345
        self.y_pos = 375
        self.dx = 0
        self.dy = 0
        self.texture_num = 0
        self.set_texture()
        self.show()

    def update_car(self, speed, x_change, y_change):
        self.move(speed, x_change, y_change)
        if self.x_pos > SCREEN_WIDTH - self.width:
            self.x_pos = SCREEN_WIDTH - self.width
        if self.x_pos < 0:
            self.x_pos = 0
        if self.y_pos > SCREEN_HEIGHT - self.height:
            self.y_pos = SCREEN_HEIGHT - self.height
        if self.y_pos < 0:
            self.y_pos = 0

    def show(self):
        screen.blit(self.texture, (self.x_pos, self.y_pos))

    def set_texture(self):
        if self.player:
            self.texture_num = 1
        else:
            self.texture_num = random.randint(2, 6)
        texture_path = os.path.join("Assets", f"car_{self.texture_num}.png")
        self.texture = pygame.image.load(texture_path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    def move(self, speed, dx, dy):
        self.dx, self.dy = dx, dy
        self.x_pos += self.dx * speed
        self.y_pos += self.dy * speed


# Game class
class Game:

    def __init__(self):
        self.bg = [Background(y=0), Background(y=SCREEN_HEIGHT)]
        self.player_car = Car(player_state="yes")
        self.speed = 3


# Main loop function
def main():
    game = Game()
    player = game.player_car
    speed = game.speed
    direction = None

    clock = pygame.time.Clock()
    while True:

        # Showing background
        for bg in game.bg:
            bg.update_bg(-game.speed)
            bg.show()

        # Showing player car
        player.show()

        # event checking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # movement of car
            held_key = pygame.key.get_pressed()

            if held_key[pygame.K_w] or held_key[pygame.K_UP]:
                player.update_car(speed, 0, -1)
            if held_key[pygame.K_a] or held_key[pygame.K_LEFT]:
                player.update_car(speed, -1, 0)
            if held_key[pygame.K_s] or held_key[pygame.K_DOWN]:
                player.update_car(speed, 0, 1)
            if held_key[pygame.K_d] or held_key[pygame.K_RIGHT]:
                player.update_car(speed, 1, 0)

        clock.tick(80)
        pygame.display.update()


# main routine
main()
