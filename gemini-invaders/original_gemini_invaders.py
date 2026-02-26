import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gemini Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Player
player_size = 50
player = pygame.Rect(WIDTH//2 - player_size//2, HEIGHT - 60, player_size, player_size)
player_speed = 5

# Bullet
bullet_speed = 7
bullets = []

# Enemy
enemy_size = 40
enemy_speed_base = 2
enemies = []

# Gemini AI Behavior Simulation
def gemini_decide_behavior():
    """Simulates Gemini AI decision for enemy behavior"""
    behavior = random.choice([
        {"speed": 3, "pattern": "charge"},
        {"speed": 1, "pattern": "flock"},
        {"speed": 2, "pattern": "retreat"},
    ])
    return behavior

def spawn_enemy():
    x = random.randint(50, WIDTH-50)
    behavior = gemini_decide_behavior()
    enemy = {"rect": pygame.Rect(x, 0, enemy_size, enemy_size), "behavior": behavior}
    enemies.append(enemy)

# Spawn initial enemies
for _ in range(5):
    spawn_enemy()

# Main game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player.x + player_size//2 - 5, player.y, 10, 20))

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.x < WIDTH - player_size:
        player.x += player_speed

    # Update bullets
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Update enemies
    for enemy in enemies[:]:
        behavior = enemy["behavior"]
        if behavior["pattern"] == "charge":
            enemy["rect"].y += behavior["speed"]
        elif behavior["pattern"] == "flock":
            # simple flock: move down slowly, move left/right randomly
            enemy["rect"].y += behavior["speed"]
            enemy["rect"].x += random.choice([-1, 1])
        elif behavior["pattern"] == "retreat":
            # fake retreat: move up slowly if near player
            if enemy["rect"].y < HEIGHT // 2:
                enemy["rect"].y += behavior["speed"]
            else:
                enemy["rect"].y -= behavior["speed"]

        # Collision with bullets
        for bullet in bullets[:]:
            if enemy["rect"].colliderect(bullet):
                bullets.remove(bullet)
                enemies.remove(enemy)
                spawn_enemy()

        # Remove enemies if out of screen
        if enemy["rect"].y > HEIGHT or enemy["rect"].y < 0:
            enemies.remove(enemy)
            spawn_enemy()

    # Draw player
    pygame.draw.rect(screen, BLUE, player)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy["rect"])

    pygame.display.flip()

pygame.quit()
