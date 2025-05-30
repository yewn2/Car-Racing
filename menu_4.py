"""
Menu version 3
This is the fourth version of the menu screen.
The credits screen has been created.
"""

# imports
import pygame
import os
import sys
import threading
import racing_5 as racer  # will be changed later to a newer version of game

# LINES 10 TO 35 NOT NECESSARY FOR MAIN PROGRAM; HOWEVER THEY ARE NEEDED FOR RUNNING INDEPENDENTLY

# size constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()
pygame.mixer.init()

# setting up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon_path = os.path.join("Assets", "game_icon.png")
game_icon = pygame.image.load(icon_path)
pygame.display.set_icon(game_icon)

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


# Button class, can also double as an image
class Button:

    def __init__(self, texture, x, y, width, height, texture2=None, in_menu=True):
        self.width = width
        self.height = height
        self.rect = None
        self.texture_name = texture
        self.texture = None
        self.texture_2_name = texture2
        self.texture_2 = None
        self.second_texture = False
        self.in_menu = in_menu
        self.set_texture(x, y)

    def set_texture(self, x, y):
        if self.in_menu:
            texture_path = os.path.join("Assets", "menu", f"{self.texture_name}.png")
        else:
            texture_path = os.path.join("Assets", f"{self.texture_name}.png")
        self.texture = pygame.image.load(texture_path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))
        self.rect = self.texture.get_rect()
        self.rect.x = x
        self.rect.y = y

        if self.texture_2_name is not None:
            texture_2_path = os.path.join("Assets", "menu", f"{self.texture_2_name}.png")
            self.texture_2 = pygame.image.load(texture_2_path)
            self.texture_2 = pygame.transform.scale(self.texture_2, (self.width, self.height))

    def show(self):
        if not self.second_texture:
            screen.blit(self.texture, self.rect)
        else:
            screen.blit(self.texture_2, self.rect)

    def check_input(self, mouse_pos):
        if (mouse_pos[0] in range(self.rect.left, self.rect.right)
                and mouse_pos[1] in range(self.rect.top, self.rect.bottom)):
            if self.texture_2 is not None:
                self.change_texture()
            return True
        return False

    def change_texture(self):
        self.second_texture = not self.second_texture


# Start menu class
class Start:

    def __init__(self):
        self.logo = Button("racing_logo", 25, 25, 750, 200)
        self.start_button = Button("start_button", 25, 325, 350, 105)
        self.options_button = Button("option_button", 425, 325, 350, 105)
        self.credits_button = Button("credits_button", 25, 475, 350, 105)
        self.quit_button = Button("quit_button", 425, 475, 350, 105)
        self.screen_options = Options()


    def start(self):
        speed_mult = 0
        if self.screen_options.speed == "slow":
            speed_mult = 0.25
        if self.screen_options.speed == "medium":
            speed_mult = 1
        if self.screen_options.speed == "fast":
            speed_mult = 2
        racer.racing_game(self.screen_options.colour, speed_mult, self.screen_options.speed.upper())

    def options(self):
        pygame.display.set_caption("-- Options --")

        while True:

            choices = self.screen_options

            clock = pygame.time.Clock()

            screen.fill(grey)

            mouse_position = pygame.mouse.get_pos()

            # Car speed
            choices.traffic_speed_image.show()
            choices.back_button.show()
            choices.slow_speed.show()
            choices.med_speed.show()
            choices.fast_speed.show()

            # Car colour
            choices.car_colour_image.show()
            choices.car_selector.show()
            choices.red_car.show()
            choices.green_car.show()
            choices.blue_car.show()
            choices.orange_car.show()
            choices.purple_car.show()
            choices.cyan_car.show()

            # Sound options
            choices.sound_button.show()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if choices.back_button.check_input(mouse_position):
                        menu_screen(self)
                    if choices.slow_speed.check_input(mouse_position):
                        choices.untick_speed("slow")
                    if choices.med_speed.check_input(mouse_position):
                        choices.untick_speed("medium")
                    if choices.fast_speed.check_input(mouse_position):
                        choices.untick_speed("fast")

                    if choices.red_car.check_input(mouse_position):
                        choices.colour = "1"
                        choices.select_car(choices.red_car)
                    if choices.green_car.check_input(mouse_position):
                        choices.colour = "2"
                        choices.select_car(choices.green_car)
                    if choices.blue_car.check_input(mouse_position):
                        choices.colour = "3"
                        choices.select_car(choices.blue_car)
                    if choices.orange_car.check_input(mouse_position):
                        choices.colour = "4"
                        choices.select_car(choices.orange_car)
                    if choices.purple_car.check_input(mouse_position):
                        choices.colour = "5"
                        choices.select_car(choices.purple_car)
                    if choices.cyan_car.check_input(mouse_position):
                        choices.colour = "6"
                        choices.select_car(choices.cyan_car)

                    if choices.sound_button.check_input(mouse_position):
                        choices.sound_on = not choices.sound_on
                        if choices.sound_on:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()

            clock.tick(80)
            pygame.display.update()

    def credits(self):
        pygame.display.set_caption("-- Credits --")

        credit_image = Credits(y=SCREEN_HEIGHT)

        while True:

            clock = pygame.time.Clock()

            screen.fill(black)

            credit_image.update_credits(1)
            credit_image.show()

            if credit_image.y_pos < -1000:
                pygame.time.wait(5000)
                menu_screen(self)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            clock.tick(80)
            pygame.display.update()


# Options menu class
class Options:

    def __init__(self):
        self.back_button = Button("back", 665, 5, 130, 50)

        # Car speed buttons/variables
        self.speed = "slow"
        self.traffic_speed_image = Button("traffic_speed", 10, 15, 435, 50)
        self.slow_speed = Button("slow_unticked", 25, 90, 240, 40, "slow_ticked")
        self.slow_speed.second_texture = True
        self.med_speed = Button("medium_unticked", 25, 145, 300, 40, "medium_ticked")
        self.fast_speed = Button("fast_unticked", 25, 200, 190, 40, "fast_ticked")

        # Car colour buttons/variables
        self.colour = "1"
        self.car_colour_image = Button("car_colour", 40, 375, 230, 50)
        self.car_selector = Button("car_selector", 40, 440, 84, 148)
        self.red_car = Button("car_1", 50, 450, 64, 128, in_menu=False)
        self.green_car = Button("car_2", 170, 450, 64, 128, in_menu=False)
        self.blue_car = Button("car_3", 300, 450, 64, 128, in_menu=False)
        self.orange_car = Button("car_4", 425, 450, 64, 128, in_menu=False)
        self.purple_car = Button("car_5", 550, 450, 64, 128, in_menu=False)
        self.cyan_car = Button("car_6", 675, 450, 64, 128, in_menu=False)

        # Sound buttons/variables
        self.sound_on = True
        self.sound_button = Button("sound", 600, 250, 55, 55, "mute")

    def untick_speed(self, new_speed):
        self.speed = new_speed
        if self.speed == "slow":
            self.slow_speed.second_texture = True
            self.med_speed.second_texture = False
            self.fast_speed.second_texture = False
        if self.speed == "medium":
            self.slow_speed.second_texture = False
            self.med_speed.second_texture = True
            self.fast_speed.second_texture = False
        if self.speed == "fast":
            self.slow_speed.second_texture = False
            self.med_speed.second_texture = False
            self.fast_speed.second_texture = True

    def select_car(self, new_car):
        self.car_selector.rect.x = new_car.rect.x - 10
        self.car_selector.rect.y = new_car.rect.y - 10


# Credits class
class Credits:
    def __init__(self, y):
        self.texture = None
        self.width = SCREEN_WIDTH
        self.height = 1800
        self.y_pos = y
        self.set_texture()
        self.show()

    # Making credits self scroll
    def update_credits(self, cy):
        self.y_pos -= cy
        if self.y_pos >= SCREEN_HEIGHT:
            self.y_pos = -SCREEN_HEIGHT

    # Displaying credits
    def show(self):
        screen.blit(self.texture, (0, self.y_pos))

    # Loading credits and transforming to appropriate size
    def set_texture(self):
        path = os.path.join("Assets", "menu", "credits.png")
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))


def menu_setup():

    menu = Start()
    music_path = os.path.join("Assets", "music.flac")
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play()
    menu_screen(menu)


def menu_screen(menu):

    pygame.display.set_caption("-- Menu --")
    screen.fill(grey)

    menu.logo.show()
    menu.start_button.show()
    menu.options_button.show()
    menu.credits_button.show()
    menu.quit_button.show()

    while True:

        clock = pygame.time.Clock()

        mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu.start_button.check_input(mouse_position):
                    menu.start()
                if menu.options_button.check_input(mouse_position):
                    menu.options()
                if menu.credits_button.check_input(mouse_position):
                    menu.credits()
                if menu.quit_button.check_input(mouse_position):
                    pygame.quit()
                    sys.exit()

        clock.tick(80)
        pygame.display.update()


# main routine
if __name__ == "__main__":
    menu_setup()
