import pygame
from pygame.locals import *
import random
import time
import sys
import os

# Constants in game
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 960
BLOCK_SIZE = 32

# Colours
WHITE = (255, 255, 255)
GREY = (64, 64, 64)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Global Variables
paused = False
score = 0
highScore = 0

# Creates Highscore file if it does not exist
highScore_path = os.path.join(os.path.dirname(__file__), 'Highscore.txt')
time.sleep(0.1)
if not os.path.exists(highScore_path):
    with open(highScore_path, 'w') as file:
        file.write('0')
        ('File not found. Created Highscore.txt')
else:
    print('File found successfully')
    with open(highScore_path, "r") as file:
        highScore = (file.read())
        print(highScore)

# Initialise Pygame
pygame.init()

# Setup game window
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake')

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)]
        self.direction = pygame.K_UP

    def move(self):
        x, y = self.positions[0]
        if self.direction == pygame.K_UP:
            y -= BLOCK_SIZE
        elif self.direction == pygame.K_DOWN:
            y += BLOCK_SIZE
        elif self.direction == pygame.K_LEFT:
            x -= BLOCK_SIZE
        elif self.direction == pygame.K_RIGHT:
            x += BLOCK_SIZE
        self.positions.insert(0, (x, y))
        if len(self.positions) > self.length:
                self.positions.pop()
            
    def turn(self, direction):
        if direction == pygame.K_UP and self.direction != pygame.K_DOWN:
            self.direction = direction
        elif direction == pygame.K_DOWN and self.direction != pygame.K_UP:
            self.direction = direction
        elif direction == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
            self.direction = direction
        elif direction == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
            self.direction = direction
    
    def draw(self, surface):
            for position in self.positions:
                rect = pygame.Rect(position[0], position[1], BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(surface, WHITE, rect)

# Food class
class Food:
    def __init__(self):
        self.position = self.generate_new_position()

    def generate_new_position(self):
        while True:
            x = random.randrange(0, WINDOW_WIDTH, BLOCK_SIZE)
            y = random.randrange(0, WINDOW_HEIGHT, BLOCK_SIZE)
            if (x, y) not in snake.positions:
                return (x, y)
    
    def draw(self, surface):
        rect = pygame.Rect(self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(surface, RED, rect)

# Set up the clock for the game loop
clock = pygame.time.Clock()

# Idk I had to initialise again
pygame.init()

# Logo/icon setup
logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')
logo_surface = pygame.image.load(logo_path)
scaled_logo_surface = pygame.transform.scale(logo_surface, (30*24, 7*24))
icon_path = os.path.join(os.path.dirname(__file__), 'Icon.png')
icon_surface = pygame.image.load(icon_path)
pygame.display.set_icon(icon_surface)

# Font setup
font_path = os.path.join(os.path.dirname(__file__), 'Arcadepix.ttf')
score_font = pygame.font.Font(font_path, 50)

# Score display function
def display_score(score):
    score_surface = score_font.render('Score: ' + str(score), True, GREY)
    game_window.blit(score_surface, (WINDOW_WIDTH - 330, 30))

# Highscore display function
def display_highScore(highScore):
    with open(highScore_path) as file:
        highScore = file.readline()
    score_surface = score_font.render('Highscore: ' + str(highScore), True, GREY)
    game_window.blit(score_surface, (30, 30))

def display_other():
    other_surface = score_font.render('Arrows to move', True, GREY)
    game_window.blit(other_surface, (50, 500))
    other_surface = score_font.render('Q to pause', True, GREY)
    game_window.blit(other_surface, (50, 550))
    other_surface = score_font.render('E to exit', True, GREY)
    game_window.blit(other_surface, (50, 600))
    other_surface = score_font.render('R to (re) start', True, GREY)
    game_window.blit(other_surface, (50, 650))

    other_surface = score_font.render('Made by Tovin B', True, GREY)
    game_window.blit(other_surface, (WINDOW_WIDTH//2-50, 500))
    other_surface = score_font.render('Font by Reekee D', True, GREY)
    game_window.blit(other_surface, (WINDOW_WIDTH//2-50, 550))
    
# Main game loop
def game():
    global food
    global snake
    global paused
    global score
    global highScore
    snake = Snake()
    food = Food()
    game_over = False
    game_window.fill(BLACK)
    food.draw(game_window)
    snake.draw(game_window)
    display_score(0)
    pygame.display.update()
    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                elif event.key == pygame.K_q:
                    paused = not paused
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    snake.turn(event.key)

        if not paused:
            game_window.fill(BLACK)
            food.draw(game_window)
            snake.draw(game_window)
            display_score(snake.length - 1)
            pygame.display.update()
    
            # Move the Snake
            snake.move()
    
            # Check for collision with Food
            if snake.positions[0] == food.position:
                snake.length += 1
                food = Food()
    
            # Check for collision with walls or self
            if snake.positions[0][0] < 0 or snake.positions[0][0] > WINDOW_WIDTH - BLOCK_SIZE or \
            snake.positions[0][1] < 0 or snake.positions[0][1] > WINDOW_HEIGHT - BLOCK_SIZE or snake.positions[0] in snake.positions[1:]:
                score = snake.length - 1
                if score > int(highScore):
                    temp = highScore
                    highScore = score
                    with open(highScore_path, 'w') as file:
                        file.write(str(highScore))
                        print(f'High score updated from {temp} to {highScore}')
                game_over = True

            # Game clock
            clock.tick(20)
    
        else:
            pause_surface = score_font.render('Paused', True, GREY)
            game_window.blit(pause_surface, (WINDOW_WIDTH//2 - 60, WINDOW_HEIGHT//2))
            pygame.display.update()
            clock.tick(5)
    menu()

# Main menu
def menu():
    global score
    global highScore
    game_window.fill(BLACK)
    display_score(score)
    display_highScore(highScore)
    display_other()
    game_window.blit(scaled_logo_surface, (325, 200))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    pygame.quit()
                elif event.key == pygame.K_r:
                    game()
        clock.tick(5)

menu()
