import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout Game')

# Clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)

# Paddle settings
paddle_width = 100
paddle_height = 10
paddle_speed = 10

# Ball settings
ball_radius = 10
ball_speed_x = 5 * random.choice([1, -1])
ball_speed_y = -5

# Brick settings
brick_rows = 6
brick_cols = 10
brick_width = 75
brick_height = 20
brick_padding = 5
brick_offset_top = 50
brick_offset_left = 50

# Initialize paddle
paddle = pygame.Rect(screen_width // 2 - paddle_width // 2, screen_height - 30, paddle_width, paddle_height)

# Initialize ball
ball = pygame.Rect(screen_width // 2, screen_height // 2, ball_radius * 2, ball_radius * 2)

# Generate bricks
def generate_bricks():
    bricks = []
    for row in range(brick_rows):
        brick_row = []
        for col in range(brick_cols):
            brick_x = brick_offset_left + col * (brick_width + brick_padding)
            brick_y = brick_offset_top + row * (brick_height + brick_padding)
            brick = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
            brick_row.append(brick)
        bricks.append(brick_row)
    return bricks

bricks = generate_bricks()

# Game states
game_active = False
game_over = False
score = 0
player_name = "Player"  # You can modify this to accept player input

# Draw the Start Menu
def draw_start_menu():
    screen.fill(BLACK)
    title_text = font.render("Welcome to Breakout!", True, WHITE)
    start_text = font.render("Press ENTER to Start", True, WHITE)
    name_text = font.render(f"Player: {player_name}", True, WHITE)

    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 200))
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, 300))
    screen.blit(name_text, (screen_width // 2 - name_text.get_width() // 2, 400))

    pygame.display.flip()

# Draw Game Over Menu
def draw_game_over_menu():
    screen.fill(BLACK)
    over_text = font.render("Game Over", True, WHITE)
    restart_text = font.render("Press R to Restart", True, WHITE)
    final_score_text = font.render(f"Final Score: {score}", True, WHITE)

    screen.blit(over_text, (screen_width // 2 - over_text.get_width() // 2, 200))
    screen.blit(final_score_text, (screen_width // 2 - final_score_text.get_width() // 2, 300))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, 400))

    pygame.display.flip()

# Draw Score on Screen
def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Game loop
def game_loop():
    global ball_speed_x, ball_speed_y, game_active, score, game_over, bricks

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not game_active and not game_over:
                    if event.key == pygame.K_RETURN:
                        game_active = True
                elif game_over:
                    if event.key == pygame.K_r:
                        # Reset game
                        game_active = False
                        game_over = False
                        ball.x = screen_width // 2
                        ball.y = screen_height // 2
                        ball_speed_x = 5 * random.choice([1, -1])
                        ball_speed_y = -5
                        bricks = generate_bricks()
                        score = 0

        if game_active:
            # Move the paddle
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and paddle.left > 0:
                paddle.move_ip(-paddle_speed, 0)
            if keys[pygame.K_RIGHT] and paddle.right < screen_width:
                paddle.move_ip(paddle_speed, 0)

            # Move the ball
            ball.x += ball_speed_x
            ball.y += ball_speed_y

            # Ball collision with walls
            if ball.left <= 0 or ball.right >= screen_width:
                ball_speed_x = -ball_speed_x
            if ball.top <= 0:
                ball_speed_y = -ball_speed_y
            if ball.bottom >= screen_height:
                # Game over
                game_active = False
                game_over = True

            # Ball collision with paddle
            if ball.colliderect(paddle):
                ball_speed_y = -ball_speed_y

            # Ball collision with bricks
            for row in bricks:
                for brick in row:
                    if ball.colliderect(brick):
                        ball_speed_y = -ball_speed_y
                        row.remove(brick)
                        score += 10
                        break

            # Clear the screen
            screen.fill(BLACK)

            # Draw the paddle
            pygame.draw.rect(screen, BLUE, paddle)

            # Draw the ball
            pygame.draw.ellipse(screen, WHITE, ball)

            # Draw the bricks
            for row in bricks:
                for brick in row:
                    pygame.draw.rect(screen, RED, brick)

            # Draw the score
            draw_score()

            # Update the screen
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(60)

        elif not game_active and not game_over:
            draw_start_menu()
        elif game_over:
            draw_game_over_menu()

if __name__ == "__main__":
    game_loop()
