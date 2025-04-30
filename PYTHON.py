import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Egg Catcher")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Basket properties
basket_width = 100
basket_height = 20
basket_x = width // 2 - basket_width // 2
basket_y = height - 50
basket_speed = 10

# Egg properties
egg_width = 30
egg_height = 40
egg_speed = 5
eggs = []  # List to store eggs

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game variables
game_over = False
clock = pygame.time.Clock()

# Functions
def create_egg():
    x = random.randint(egg_width // 2, width - egg_width // 2)
    y = -egg_height # Start above the screen
    eggs.append({"x": x, "y": y})

def draw_basket():
    pygame.draw.rect(screen, white, (basket_x, basket_y, basket_width, basket_height))

def draw_eggs():
    for egg in eggs:
        pygame.draw.ellipse(screen, white, (egg["x"] - egg_width // 2, egg["y"], egg_width, egg_height))  # Draw egg as ellipse

def move_eggs():
    for egg in eggs:
        egg["y"] += egg_speed

def check_collisions():
    global score, game_over
    for i in range(len(eggs) - 1, -1, -1):  # Iterate backwards for safe removal
        egg = eggs[i]
        egg_rect = pygame.Rect(egg["x"] - egg_width // 2, egg["y"], egg_width, egg_height)
        basket_rect = pygame.Rect(basket_x, basket_y, basket_width, basket_height)

        if egg_rect.colliderect(basket_rect):
            score += 1
            eggs.pop(i) # Remove the caught egg
        elif egg["y"] > height:  # Egg missed
            eggs.pop(i)
            if not game_over: # Only trigger game over once
                game_over = True



def display_score():
    score_text = font.render("Score: " + str(score), True, white)
    screen.blit(score_text, (10, 10))

def display_game_over():
    game_over_text = font.render("Game Over! Press SPACE to Retry", True, red)
    text_rect = game_over_text.get_rect(center=(width // 2, height // 2))
    screen.blit(game_over_text, text_rect)

# Game loop
running = True
egg_timer = 0
egg_interval = 50  # Milliseconds between egg creation

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:  # Retry
                game_over = False
                score = 0
                eggs = []  # Clear existing eggs
                basket_x = width // 2 - basket_width // 2 # Reset basket position
    # Basket movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < width - basket_width:
        basket_x += basket_speed

    # Egg creation
    egg_timer += clock.get_rawtime()
    if egg_timer > egg_interval:
        create_egg()
        egg_timer = 0

    # Game logic
    move_eggs()
    check_collisions()

    # Drawing
    screen.fill(black)
    draw_basket()
    draw_eggs()
    display_score()

    if game_over:
        display_game_over()

    pygame.display.flip()
    clock.tick(60)  # Control frame rate

pygame.quit()