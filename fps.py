import pygame
import math
import random

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
HALF_HEIGHT = HEIGHT // 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Raycasting FPS in Pure Python")
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DARKGRAY = (40, 40, 40)

# Map layout
MAP = [
    '1111111111',
    '1        1',
    '1   11   1',
    '1        1',
    '1111111111'
]
TILE = 100
MAP_WIDTH = len(MAP[0]) * TILE
MAP_HEIGHT = len(MAP) * TILE

# Player setup
player_x, player_y = 150, 150
player_angle = 0
player_speed = 3
rotation_speed = 0.04
score = 0

# Enemies
enemies = []
for _ in range(5):
    while True:
        x = random.randint(1, len(MAP[0]) - 2) * TILE + TILE // 2
        y = random.randint(1, len(MAP) - 2) * TILE + TILE // 2
        if MAP[y // TILE][x // TILE] == ' ':
            enemies.append([x, y])
            break

def draw_map():
    for y, row in enumerate(MAP):
        for x, char in enumerate(row):
            if char == '1':
                pygame.draw.rect(screen, DARKGRAY, (x*TILE, y*TILE, TILE, TILE))
    pygame.draw.circle(screen, BLUE, (int(player_x), int(player_y)), 8)
    for ex, ey in enemies:
        pygame.draw.circle(screen, RED, (int(ex), int(ey)), 6)

def cast_rays():
    num_rays = 120
    fov = math.pi / 3
    start_angle = player_angle - fov / 2
    delta_angle = fov / num_rays

    ray_angle = start_angle
    for ray in range(num_rays):
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)
        for depth in range(1, 1000):
            target_x = player_x + depth * cos_a
            target_y = player_y + depth * sin_a
            i, j = int(target_x / TILE), int(target_y / TILE)
            if 0 <= i < len(MAP[0]) and 0 <= j < len(MAP):
                if MAP[j][i] == '1':
                    wall_height = 30000 / (depth + 0.1)
                    brightness = 255 / (1 + depth * depth * 0.0001)
                    pygame.draw.rect(
                        screen,
                        (brightness, brightness, brightness),
                        (ray * (WIDTH // num_rays), HALF_HEIGHT - wall_height // 2,
                         WIDTH // num_rays, wall_height)
                    )
                    break
        ray_angle += delta_angle

def move_player():
    global player_x, player_y, player_angle
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]: player_angle -= rotation_speed
    if keys[pygame.K_RIGHT]: player_angle += rotation_speed

    sin_a = math.sin(player_angle)
    cos_a = math.cos(player_angle)

    if keys[pygame.K_w]:
        dx = cos_a * player_speed
        dy = sin_a * player_speed
        if MAP[int((player_y + dy) // TILE)][int((player_x + dx) // TILE)] == ' ':
            player_x += dx
            player_y += dy
    if keys[pygame.K_s]:
        dx = cos_a * player_speed
        dy = sin_a * player_speed
        if MAP[int((player_y - dy) // TILE)][int((player_x - dx) // TILE)] == ' ':
            player_x -= dx
            player_y -= dy
    if keys[pygame.K_a]:
        dx = sin_a * player_speed
        dy = -cos_a * player_speed
        if MAP[int((player_y + dy) // TILE)][int((player_x + dx) // TILE)] == ' ':
            player_x += dx
            player_y += dy
    if keys[pygame.K_d]:
        dx = -sin_a * player_speed
        dy = cos_a * player_speed
        if MAP[int((player_y + dy) // TILE)][int((player_x + dx) // TILE)] == ' ':
            player_x += dx
            player_y += dy

def shoot():
    global score
    sin_a = math.sin(player_angle)
    cos_a = math.cos(player_angle)

    for depth in range(1, 1000):
        target_x = player_x + depth * cos_a
        target_y = player_y + depth * sin_a
        for i, (ex, ey) in enumerate(enemies):
            if math.hypot(target_x - ex, target_y - ey) < 10:
                del enemies[i]
                score += 1
                return

# Main loop
running = True
while running:
    screen.fill(BLACK)
    move_player()
    cast_rays()
    draw_map()

    # HUD
    font = pygame.font.SysFont("Arial", 30)
    screen.blit(font.render(f"Score: {score}", True, WHITE), (20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            shoot()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
