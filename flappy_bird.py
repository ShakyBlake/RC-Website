import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
GAP = 200
GRAVITY = 0.5
BIRD_JUMP = -8
PIPE_SPEED = 3
FPS = 60

# Colors
YELLOW = (230, 251, 45)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
BLUE = (34, 191, 170)

# File to store high score
HIGH_SCORE_FILE = "highscore.txt"

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
bg = pygame.image.load("background_image.png")

# Bird class
class Bird:
    def __init__(self):
        self.x = 60
        self.y = SCREEN_HEIGHT // 2
        self.y_velocity = 0

    def draw(self):
        pygame.draw.rect(screen, YELLOW, [self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT])

    def update(self):
        self.y_velocity += GRAVITY
        self.y += self.y_velocity

    def jump(self):
        self.y_velocity = BIRD_JUMP

# Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(150, 450)
        self.passed = False

    def draw(self):
        pygame.draw.rect(screen, GREEN, [self.x, self.height, PIPE_WIDTH, PIPE_HEIGHT])
        pygame.draw.rect(screen, GREEN, [self.x, self.height - GAP - PIPE_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT])

    def update(self):
        self.x -= PIPE_SPEED

# Reset function
def reset():
    return Bird(), []

# Get high score from file
def get_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Save high score to file
def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

# Main function
def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = []
    score = 0
    high_score = get_high_score()
    game_over = False

    while True:
        while not game_over:
            # Game loop

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.jump()

            bird.update()
            bird.draw()

            if len(pipes) == 0 or pipes[-1].x < SCREEN_WIDTH - 200:
                pipes.append(Pipe())

            for pipe in pipes:
                pipe.update()
                pipe.draw()

                if not pipe.passed and pipe.x + PIPE_WIDTH < bird.x:
                    pipe.passed = True
                    score += 1
                    if score > high_score:
                        high_score = score

                if pipe.x + PIPE_WIDTH < 0:
                    pipes.remove(pipe)

                # Collision detection
                if (bird.y < 0 or bird.y + BIRD_HEIGHT > SCREEN_HEIGHT or
                    (bird.x + BIRD_WIDTH > pipe.x and bird.x < pipe.x + PIPE_WIDTH and
                    (bird.y < pipe.height - GAP or bird.y + BIRD_HEIGHT > pipe.height))):
                    game_over = True

            # Display score
            font = pygame.font.SysFont(None, 36)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(FPS)

        # Game over loop
        font = pygame.font.SysFont(None, 36)
        game_over_text = font.render("Game Over. Press R to restart.", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    bird, pipes = reset()
                    score = 0
                    game_over = False
                    break

        # Update high score if needed
        if score > high_score:
            high_score = score
            save_high_score(high_score)

if __name__ == "__main__":
    main()