import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and Icon
pygame.display.set_caption("Space Invaders")

# Player
player_color = (0, 255, 0)  # Green
player_width = 64
player_height = 64
player_x = screen_width / 2 - player_width / 2
player_y = screen_height - 100
player_x_change = 0

# Enemy
enemy_color = (255, 0, 0)  # Red
enemy_width = 64
enemy_height = 64
enemy_x = random.randint(0, screen_width - enemy_width)
enemy_y = random.randint(50, 150)
enemy_x_change = 4
enemy_y_change = 40

# Bullet
bullet_color = (255, 255, 255)  # White
bullet_width = 5
bullet_height = 20
bullet_x = 0
bullet_y = player_y
bullet_y_change = 10
bullet_state = "ready"

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

def show_score(x, y):
    score_value = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))

def player(x, y):
    pygame.draw.rect(screen, player_color, (x, y, player_width, player_height))

def enemy(x, y):
    pygame.draw.rect(screen, enemy_color, (x, y, enemy_width, enemy_height))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    pygame.draw.rect(screen, bullet_color, (x + player_width / 2 - bullet_width / 2, y, bullet_width, bullet_height))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = ((enemy_x + enemy_width / 2 - bullet_x)**2 + (enemy_y + enemy_height / 2 - bullet_y)**2)**0.5
    return distance < 27

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # RGB Background
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keystroke controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x + player_width / 2 - bullet_width / 2
                    bullet_y = player_y
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= screen_width - player_width:
        player_x = screen_width - player_width

    # Enemy movement
    enemy_x += enemy_x_change
    if enemy_x <= 0:
        enemy_x_change = 4
        enemy_y += enemy_y_change
    elif enemy_x >= screen_width - enemy_width:
        enemy_x_change = -4
        enemy_y += enemy_y_change

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    if bullet_y <= 0:
        bullet_y = player_y
        bullet_state = "ready"

    # Collision
    collision = is_collision(enemy_x, enemy_y, bullet_x, bullet_y)
    if collision:
        bullet_y = player_y
        bullet_state = "ready"
        score += 1
        enemy_x = random.randint(0, screen_width - enemy_width)
        enemy_y = random.randint(50, 150)

    player(player_x, player_y)
    enemy(enemy_x, enemy_y)
    show_score(text_x, text_y)

    pygame.display.update()
