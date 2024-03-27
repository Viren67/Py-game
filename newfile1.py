import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Get screen dimensions dynamically
infoObject = pygame.display.Info()
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h

# Function to generate random color
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
GRAVITY = 0.35
FLAP_STRENGTH = -5

# Classes
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 4
        self.velocity = 0
        self.image = pygame.image.load('/storage/emulated/0/.py/pngwing.com (1).png')
        self.image = pygame.transform.scale(self.image, (120, 90))

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self, screen):
        screen.blit(self.image, (self.x, int(self.y)))

class PipePair:
    def __init__(self):
        self.x = SCREEN_WIDTH + 100
        self.gap_y = random.randint(200, 400)
        self.pipe_width = 110
        self.pipe_height = SCREEN_HEIGHT - self.gap_y - 200
        self.passed = False
        self.color = random_color()

    def move(self):
        self.x -= 5

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, 0, self.pipe_width, self.gap_y))
        pygame.draw.rect(screen, self.color, (self.x, self.gap_y + 300, self.pipe_width, self.pipe_height))

    def collides_with(self, bird):
        bird_rect = bird.image.get_rect(topleft=(bird.x, bird.y))
        pipe_rect_top = pygame.Rect(self.x, 0, self.pipe_width, self.gap_y)
        pipe_rect_bottom = pygame.Rect(self.x, self.gap_y + 300, self.pipe_width, self.pipe_height)
        return bird_rect.colliderect(pipe_rect_top) or bird_rect.colliderect(pipe_rect_bottom)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('/storage/emulated/0/.py/pngwing.com (1).png')

clock = pygame.time.Clock()

bird = Bird()
pipes = []
score = 0
font = pygame.font.Font(None, 72)
game_over_font = pygame.font.Font(None, 96)
start_font = pygame.font.Font(None, 96)

# Load background image
background_image = pygame.image.load('/storage/emulated/0/.py/flappy-bird-background-gecj5m4a9yhhjp87.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Game state
START = 0
PLAYING = 1
GAME_OVER = 2
game_state = START

# Function to reset the game
def reset_game():
    global bird, pipes, score, game_state
    bird = Bird()
    pipes = []
    score = 0
    game_state = PLAYING

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == START:
                reset_game()
            elif game_state == PLAYING:
                bird.flap()
            elif game_state == GAME_OVER:
                reset_game()

    # Update
    if game_state == PLAYING:
        bird.update()

        if len(pipes) == 0 or pipes[-1].x < SCREEN_WIDTH - 200:
            pipes.append(PipePair())

        for pipe in pipes:
            pipe.move()
            if pipe.x + pipe.pipe_width < 0:
                pipes.remove(pipe)
            if pipe.collides_with(bird):
                game_state = GAME_OVER
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                score += 1

    # Drawing
    screen.blit(background_image, (0, 0))  # Draw background image
    bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)

    if game_state == START:
        start_text = start_font.render("Tap to Start", True, WHITE)
        screen.blit(start_text, ((SCREEN_WIDTH - start_text.get_width()) // 2, SCREEN_HEIGHT // 2 - 40))
    elif game_state == GAME_OVER:
        game_over_text = game_over_font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, SCREEN_HEIGHT // 2 - 40))

    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) // 2, 20))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
