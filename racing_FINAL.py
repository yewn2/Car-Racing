"""
FINAL GAMELOOP VERSION
"""

# imports
import pygame
import random
import math
import sys
import os
import menu_FINAL as menu

# size constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()

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
score_font = pygame.font.SysFont(os.path.abspath(score_font_path), 25)
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

    def __init__(self, colour):
        self.texture = None
        self.dx = 0
        self.dy = 0
        self.texture_num = colour
        self.rect = None
        self.player = True
        self.width = 75
        self.height = 150
        self.x_pos = (SCREEN_WIDTH / 2) - (self.width / 2)
        self.y_pos = 375
        self.set_texture()
        self.show()

    def update_car(self, spd, direct):
        self.move(spd, direct)
        if self.x_pos > SCREEN_WIDTH - self.width:
            self.x_pos = SCREEN_WIDTH - self.width

        if self.x_pos < 0:
            self.x_pos = 0

        if self.y_pos > SCREEN_HEIGHT - self.height:
            self.y_pos = SCREEN_HEIGHT - self.height

        if self.y_pos < 0:
            self.y_pos = 0

    def show(self):
        screen.blit(self.texture, self.rect)

    def set_texture(self):
        texture_path = os.path.join("Assets", f"car_{self.texture_num}.png")
        self.texture = pygame.image.load(texture_path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))
        self.rect = self.texture.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

    def move(self, speed, direction):
        if direction is not None:
            self.dx, self.dy = (speed * math.cos(math.radians(direction)) * 1.5,
                                -speed * math.sin(math.radians(direction)) * 1.5)
        self.x_pos += self.dx
        self.y_pos += self.dy
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos


# Random car class
class Traffic:
    def __init__(self):
        self.texture = None
        self.dy = 0
        self.texture_num = 0
        self.rect = None
        self.width = random.randint(50, 125)
        self.height = self.width * 2
        self.x_pos = random.randint(0, SCREEN_WIDTH - self.width)
        self.y_pos = 0 - self.height
        self.set_texture()

    def update_car(self, spd, mult):
        self.move(spd, mult)
        if self.y_pos > SCREEN_HEIGHT:
            return True
        return False

    def show(self):
        screen.blit(self.texture, self.rect)

    def set_texture(self):
        self.texture_num = random.randint(1, 6)
        texture_path = os.path.join("Assets", f"car_{self.texture_num}.png")
        self.texture = pygame.image.load(texture_path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))
        self.rect = self.texture.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

    def move(self, speed, multiplier):
        self.dy = ((-speed * math.sin(math.radians(270))) +
                   (random.uniform((-speed * 2 / 3), (speed * 2)))) * multiplier
        self.y_pos += self.dy
        self.rect.y = self.y_pos


# Collision class - to detect that player car is hitting other cars
class Collision:

    def check_collision(self, object1, object2):
        return pygame.Rect.colliderect(object1, object2)


# Class to keep track of score
class Score:

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.score_label = None
        self.label = None
        self.high_label = None
        self.high_score_label = None
        self.high_score = self.fetch_high_score()
        self.current_score = 0
        self.font = score_font
        self.colour = black

    def fetch_high_score(self):
        try:
            high_score_file = open(f"{self.difficulty}_HIGH_score.txt", 'r')
        except IOError:
            high_score_file = open(f"{self.difficulty}_HIGH_score.txt", 'w')
            high_score_file.write("0")
        high_score_file = open(f"{self.difficulty}_HIGH_score.txt", 'r')
        value = high_score_file.read()
        high_score_file.close()
        return value

    def update_high_score(self):
        if int(self.current_score) > int(self.high_score):
            return self.current_score
        else:
            return self.high_score

    def save_high_score(self, high_score):
        high_score_file = open(f"{self.difficulty}_HIGH_score.txt", 'w')
        high_score_file.write(str(high_score))
        high_score_file.close()

    def update_score(self):
        self.current_score += 1

    def show_score(self):
        self.label = self.font.render("SCORE", True, self.colour)
        self.score_label = self.font.render(f"{self.current_score}", True, self.colour)
        self.high_label = self.font.render("HIGH SCORE", True, self.colour)
        self.high_score_label = self.font.render(f"{self.high_score}", True, self.colour)
        label_width = self.label.get_rect().width
        screen.blit(self.label, (SCREEN_WIDTH - label_width - 10, 10))
        screen.blit(self.score_label, (SCREEN_WIDTH - label_width + 15, 25))
        screen.blit(self.high_label, (SCREEN_WIDTH - label_width - 150, 10))
        screen.blit(self.high_score_label, (SCREEN_WIDTH - label_width - 100, 25))


# Game class
class Game:

    def __init__(self, player_colour, traffic_mult, difficulty):
        self.big_text = None
        self.small_text_1 = None
        self.small_text_2 = None
        self.bg = [Background(y=0), Background(y=SCREEN_HEIGHT)]
        self.player_car = Car(player_colour)
        self.traffic = []
        self.collision = Collision()
        self.last_spawned = 0
        self.difficulty = difficulty
        self.score = Score(self.difficulty)
        self.speed = 3
        self.traffic_speed = traffic_mult
        self.playing = True
        self.end_text()

    def car_spawn(self, loops, multiplier):
        spawn = (loops - self.last_spawned) > random.uniform((75 * (1 / multiplier)),
                                                             (125 * (1 / multiplier)))
        if spawn:
            self.last_spawned = loops
        return spawn

    def create_car(self):
        new_car = Traffic()
        self.traffic.append(new_car)

    def end_text(self):
        self.big_text = exit_font.render("G A M E  O V E R", True, black)
        self.small_text_1 = msg_font.render("Press R to restart, Q to quit or", True, black)
        self.small_text_2 = msg_font.render("B to go back to the menu", True, black)

    def start_game(self):
        self.playing = True

    def game_over(self):
        screen.fill(grey)
        screen.blit(self.big_text, (SCREEN_WIDTH // 2 - self.big_text.get_width() // 2,
                                    (SCREEN_HEIGHT // 4) - 50))
        screen.blit(self.small_text_1, (SCREEN_WIDTH // 2 - self.small_text_1.get_width() // 2,
                                        SCREEN_HEIGHT // 4 + self.small_text_1.get_height()))
        screen.blit(self.small_text_2, (SCREEN_WIDTH // 2 - self.small_text_2.get_width() // 2,
                                        SCREEN_HEIGHT // 4 + self.small_text_2.get_height() * 2))
        self.playing = False

    def update_speed(self):
        if self.score.current_score < 5:
            self.speed = 3
        else:
            self.speed = 3 + (self.score.current_score * 0.05)

    def restart_game(self):
        self.__init__(self.player_car.texture_num, self.traffic_speed, self.difficulty)


# Main loop function
def racing_game(colour, traffic_speed, difficulty):

    pygame.display.set_caption("Car Racing Game - by Nathan Yew")

    game = Game(colour, traffic_speed, difficulty)
    player = game.player_car
    direction = None

    clock = pygame.time.Clock()

    loops = 0

    while True:

        if game.playing:

            loops += 1
            game.update_speed()
            speed = game.speed

            # Showing background
            for bg in game.bg:
                bg.update_bg(-game.speed)
                bg.show()

            # Showing player car
            player.show()
            player.update_car(speed, direction)

            # Updating random cars
            if game.car_spawn(loops, traffic_speed):
                game.create_car()
            for car in game.traffic:
                if car.update_car(speed, traffic_speed):
                    game.traffic.pop(0)
                    game.score.update_score()
                car.show()

                # collision detection - player
                if game.collision.check_collision(player.rect, car.rect):
                    for obstacle in game.traffic:
                        obstacle.y_pos = SCREEN_HEIGHT + 1
                        obstacle.show()
                    pygame.display.update()
                    game.score.save_high_score(game.score.update_high_score())
                    game.game_over()

            # Show score
            game.score.show_score()

        # event checking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # movement of car
            if event.type == pygame.KEYDOWN:

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
                    direction = None
                    loops = 0
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_b:
                    menu.menu_setup()

        clock.tick(80)
        pygame.display.update()


# main routine
if __name__ == "__main__":
    racing_game("1", 1, "SLOW")
