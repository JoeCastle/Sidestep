import pygame
import random
from PIL import Image, ImageDraw
import os 
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
PLAYER_SIZE = 25
OBSTACLE_SIZE = 50
PLAYER_SPEED = 0.7
OBSTACLE_SPEED_MIN = 0.6
OBSTACLE_SPEED_MAX = 1.5

# Colours
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game States
START = 0
PLAYING = 1
GAME_OVER = 2

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avoid the Obstacles")

# Define player image
player_img_path = "player.png"

# Function to create a triangle surface
def create_triangle(size):
    triangle = pygame.Surface(size, pygame.SRCALPHA)
    width, height = size
    pygame.draw.polygon(triangle, RED, [(0, height), (width / 2, 0), (width, height)])
    return triangle

if os.path.exists(player_img_path):
    player_img = pygame.image.load(player_img_path)
else:
    # Create a placeholder image if 'player.png' doesn't exist
    # placeholder_image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
    # placeholder_image.fill(WHITE)
    # font = pygame.font.Font(None, 24)
    # text = font.render("Player", True, RED)
    # placeholder_image.blit(text, (10, 10))
    # player_img = placeholder_image
    player_img = create_triangle((PLAYER_SIZE, PLAYER_SIZE))

# Define obstacle image
obstacle_img_path = "obstacle.png"

if os.path.exists(obstacle_img_path):
    obstacle_img = pygame.image.load(obstacle_img_path)
else:
    # Create a placeholder image if 'obstacle.png' doesn't exist
    placeholder_image = pygame.Surface((OBSTACLE_SIZE, OBSTACLE_SIZE))
    placeholder_image.fill(RED)  # Placeholder obstacle image color
    obstacle_img = placeholder_image

# Set up game variables
player_x = WIDTH // 2 - PLAYER_SIZE // 2
player_y = HEIGHT - PLAYER_SIZE - 20
player_speed_x = 0
player_lives = 3
player_immortality = False # Duration of immortality in seconds
player_immortality_duration = 3 # Flag to indicate if the player is immortal
player_immortality_start_time = 0 # Timestamp when immortality starts
flash_interval = 0.2  # Interval for player flashing (seconds)
last_flash_time = 0  # Timestamp of the last player flash
player_visible = True

obstacle_x = random.randint(0, WIDTH - OBSTACLE_SIZE)
obstacle_y = 0
obstacle_speed = OBSTACLE_SPEED_MIN

score = 0

game_state = START

# Flags for left and right movement
moving_left = False
moving_right = False

# Game loop
running = True
while running:
    current_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Check for the "Esc" key press event
                running = False  # Set the 'running' flag to False to exit the loop when "Esc" is pressed

        if game_state == PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    moving_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    moving_right = False

    if game_state == PLAYING:
        # Determine player's horizontal speed based on movement flags
        if moving_left and not moving_right:
            player_speed_x = -PLAYER_SPEED
        elif moving_right and not moving_left:
            player_speed_x = PLAYER_SPEED
        else:
            player_speed_x = 0

        # Update player position
        player_x += player_speed_x

        # Clamp player's position within the screen boundaries
        player_x = max(0, min(player_x, WIDTH - PLAYER_SIZE))

        # Update obstacle position
        obstacle_y += obstacle_speed

        # Check for immortality
        if player_immortality:
            if current_time - player_immortality_start_time >= player_immortality_duration:
                player_immortality = False  # End immortality after the specified duration

            # Flash the player on and off at the specified interval
            if current_time - last_flash_time >= flash_interval:
                last_flash_time = current_time
                player_visible = not player_visible  # Toggle player visibility


        # Check collision
        if (
            player_x < obstacle_x + OBSTACLE_SIZE
            and player_x + PLAYER_SIZE > obstacle_x
            and player_y < obstacle_y + OBSTACLE_SIZE
            and player_y + PLAYER_SIZE > obstacle_y
            and player_immortality == False
        ):
            player_lives -= 1

            # Need to make the player immortal otherwise they would get hit multiple times per "collision".
            player_immortality = True
            player_immortality_start_time = current_time

            if (player_lives == 0):
                game_state = GAME_OVER

        # Check if obstacle is out of the screen
        if obstacle_y > HEIGHT:
            score += 1
            obstacle_x = random.randint(0, WIDTH - OBSTACLE_SIZE)
            obstacle_y = 0
            obstacle_speed = random.uniform(OBSTACLE_SPEED_MIN, OBSTACLE_SPEED_MAX)

        # Clear the screen
        screen.fill(WHITE)

        # Draw player
        # Render and display the player with adjusted transparency
        if not player_immortality:
            screen.blit(player_img, (player_x, player_y))
        elif player_visible:
            screen.blit(player_img, (player_x, player_y))

        # Draw obstacle
        screen.blit(obstacle_img, (obstacle_x, obstacle_y))

        # Display the score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, RED)
        screen.blit(score_text, (10, 10))

        # Display the lives
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f"Lives: {player_lives}", True, RED)
        screen.blit(lives_text, (280, 10))

        pygame.display.update()

    elif game_state == START:
        # Display start screen
        screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        start_text = font.render("Press SPACE to Start", True, RED)
        screen.blit(start_text, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = PLAYING
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False 

    elif game_state == GAME_OVER:
        # Display game over screen
        screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        game_over_text = font.render(f"Game Over. Your Score: {score}", True, RED)
        restart_text = font.render("Press SPACE to Restart", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2 - 50))
        screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player_x = WIDTH // 2 - PLAYER_SIZE // 2
                player_y = HEIGHT - PLAYER_SIZE
                player_speed_x = 0

                obstacle_x = random.randint(0, WIDTH - OBSTACLE_SIZE)
                obstacle_y = 0

                score = 0

                game_state = PLAYING
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False 

# Quit Pygame
pygame.quit()
