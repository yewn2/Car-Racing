"""
Car Racing Version 4 (alternate version)
Creating cars with random movements.
Implementing collision between player and car
This version is my trialled version, where I tested out implementing the random cars into the
Car class, with the player object.
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
        self.texture = None
        self.dx = 0
        self.dy = 0
        self.dx_direct = 0
        self.texture_num = 0
        self.generate_direction()
        if player_state == "yes":
            self.player = True
            self.width = 75
            self.height = 150
            self.x_pos = 345
            self.y_pos = 375
        elif player_state == "no":
            self.player = False
            self.width = random.randint(25, 70)
            self.height = self.width * 2
            self.x_pos = random.randint(0, SCREEN_WIDTH - self.width)
            self.y_pos = 0 - self.height
        self.set_texture()
        self.show()

    def update_car(self, spd, direct):
        self.move(spd, direct)
        if self.x_pos > SCREEN_WIDTH - self.width:
            self.x_pos = SCREEN_WIDTH - self.width
            if not self.player:
                self.generate_direction()
        if self.x_pos < 0:
            self.x_pos = 0
            if not self.player:
                self.generate_direction()
        if self.player:
            if self.y_pos > SCREEN_HEIGHT - self.height:
                self.y_pos = SCREEN_HEIGHT - self.height
            if self.y_pos < 0:
                self.y_pos = 0
        else:
            if self.y_pos > SCREEN_HEIGHT:
                del self

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

    def move(self, speed, direction):
        if direction is not None:
            self.dx, self.dy = (speed * math.cos(math.radians(direction)),
                                -speed * math.sin(math.radians(direction)))
        if direction is None:
            self.dx, self.dy = (speed * math.cos(math.radians(self.dx_direct)),
                                -speed * math.sin(math.radians(270)))

        self.x_pos += self.dx
        self.y_pos += self.dy

    def generate_direction(self):
        self.dx_direct = random.randint(0, 360)


# Collision class - to detect that player car is hitting other cars,
# and that random cars do not overlap
class Collision:

    def dist_between(self, object1, object2):
        distance = math.sqrt(
            (object1.x_pos - object2.x_pos) ** 2 + (object1.y_pos - object2.y_pos) ** 2)
        return distance < 90


# Game class
class Game:

    def __init__(self):
        self.big_text = None
        self.small_text = None
        self.bg = [Background(y=0), Background(y=SCREEN_HEIGHT)]
        self.player_car = Car(player_state="yes")
        self.random_cars = []
        self.collision = Collision()
        self.speed = 3
        self.playing = True
        self.end_text()

    def car_spawn(self, loops):
        return loops % (random.randint(50, 200)) == 0

    def create_car(self):
        new_car = Car(player_state="no")
        self.random_cars.append(new_car)

    def end_text(self):
        self.big_text = exit_font.render("G A M E  O V E R", True, black)
        self.small_text = msg_font.render("Press R to restart or Q to quit", True, black)

    def start_game(self):
        self.playing = True

    def game_over(self):
        screen.fill(grey)
        screen.blit(self.big_text, (SCREEN_WIDTH // 2 - self.big_text.get_width() // 2,
                                    (SCREEN_HEIGHT // 4) - 50))
        screen.blit(self.small_text, (SCREEN_WIDTH // 2 - self.small_text.get_width() // 2,
                                      SCREEN_WIDTH // 4))
        self.playing = False

    def restart_game(self):
        self.__init__()


# Main loop function
def main():
    game = Game()
    player = game.player_car
    speed = game.speed
    direction = None

    clock = pygame.time.Clock()

    loops = 0

    while True:

        if game.playing:

            loops += 1

            # Showing background
            for bg in game.bg:
                bg.update_bg(-game.speed)
                bg.show()

            # Showing player car
            player.show()
            player.update_car(speed, direction)

            # Updating random cars
            if game.car_spawn(loops):
                game.create_car()
            for car in game.random_cars:
                car.update_car(speed, None)
                car.show()

                # collision detection - player
                if game.collision.dist_between(player, car):
                    game.game_over()

                for car_2 in game.random_cars:
                    if game.random_cars.index(car) != game.random_cars.index(car_2):
                        if game.collision.dist_between(car, car_2):
                            car.dx_direct = -car.dx_direct
                            car_2.dx_direct = -car_2.dx_direct
                            car.move(speed, None)
                            car_2.move(speed, None)

        # event checking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # movement of car
            if event.type == pygame.KEYDOWN:

                if not game.playing:
                    game.start_game()

                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    direction = 90
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    direction = 180
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    direction = 270
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    direction = 0

                if event.key == pygame.K_r:
                    game.restart_game()
                    player = game.player_car
                    loops = 0
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        clock.tick(80)
        pygame.display.update()


# main routine
main()
