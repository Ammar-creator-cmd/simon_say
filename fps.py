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

# Mouse look setup
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
mouse_look_active = False

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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

# Player setup
player_x, player_y = 150, 150
player_angle = 0
player_speed = 3
score = 0
player_health = 100

# Ammo and reloading
ammo = 6
max_ammo = 6
reloading = False
reload_timer = 0

# Enemies
enemies = []
dead_enemies = []
enemy_attack_timer = 0
for _ in range(5):
    while True:
        x = random.randint(1, len(MAP[0]) - 2) * TILE + TILE // 2
        y = random.randint(1, len(MAP) - 2) * TILE + TILE // 2
        if MAP[y // TILE][x // TILE] == ' ':
            enemies.append([x, y])
            break

# Muzzle flash
muzzle_flash_timer = 0

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

    if mouse_look_active:
        mouse_dx = pygame.mouse.get_rel()[0]
        player_angle += mouse_dx * 0.002
        player_angle %= 2 * math.pi
    else:
        pygame.mouse.get_rel()

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
    global score, muzzle_flash_timer, ammo
    if reloading or ammo <= 0:
        return

    ammo -= 1
    muzzle_flash_timer = 5

    sin_a = math.sin(player_angle)
    cos_a = math.cos(player_angle)

    for depth in range(1, 1000):
        target_x = player_x + depth * cos_a
        target_y = player_y + depth * sin_a
        for i, (ex, ey) in enumerate(enemies):
            if math.hypot(target_x - ex, target_y - ey) < 10:
                dead_enemies.append([ex, ey, 15])
                del enemies[i]
                score += 1
                return

def reload():
    global reloading, reload_timer
    if not reloading and ammo < max_ammo:
        reloading = True
        reload_timer = 60

def update_reload():
    global reloading, reload_timer, ammo
    if reloading:
        reload_timer -= 1
        if reload_timer <= 0:
            ammo = max_ammo
            reloading = False

def enemy_attack():
    global player_health, enemy_attack_timer
    if enemy_attack_timer > 0:
        enemy_attack_timer -= 1
        return

    for ex, ey in enemies:
        if math.hypot(ex - player_x, ey - player_y) < 50:
            player_health -= 10
            enemy_attack_timer = 60
            break

def draw_enemies_3d():
    for ex, ey in enemies:
        dx = ex - player_x
        dy = ey - player_y
        distance = math.hypot(dx, dy)
        angle = math.atan2(dy, dx) - player_angle

        if -math.pi/6 < angle < math.pi/6:
            screen_x = WIDTH // 2 + (angle / (math.pi / 3)) * WIDTH
            size = min(5000 / (distance + 0.1), 80)
            top = HALF_HEIGHT - size // 2

            pygame.draw.rect(screen, RED, (screen_x - size // 4, top, size // 2, size))
            pygame.draw.circle(screen, WHITE, (int(screen_x), int(top)), int(size // 4))
            pygame.draw.circle(screen, BLACK, (int(screen_x - size // 8), int(top - size // 8)), int(size // 16))
            pygame.draw.circle(screen, BLACK, (int(screen_x + size // 8), int(top - size // 8)), int(size // 16))

def draw_dead_enemies():
    for enemy in dead_enemies[:]:
        ex, ey, timer = enemy
        dx = ex - player_x
        dy = ey - player_y
        distance = math.hypot(dx, dy)
        angle = math.atan2(dy, dx) - player_angle

        if -math.pi/6 < angle < math.pi/6:
            screen_x = WIDTH // 2 + (angle / (math.pi / 3)) * WIDTH
            size = min(5000 / (distance + 0.1), 80)
            top = HALF_HEIGHT - size // 2
            alpha = int(255 * (timer / 15))

            s = pygame.Surface((size // 2, size), pygame.SRCALPHA)
            pygame.draw.rect(s, (255, 0, 0, alpha), (0, 0, size // 2, size))
            screen.blit(s, (screen_x - size // 4, top))

            s2 = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(s2, (255, 255, 255, alpha), (size // 2, size // 2), size // 4)
            screen.blit(s2, (screen_x - size // 2, top - size // 4))

        enemy[2] -= 1
        if enemy[2] <= 0:
            dead_enemies.remove(enemy)

def draw_weapon():
    weapon_width, weapon_height = 60, 100
    x = WIDTH // 2 - weapon_width // 2
    y = HEIGHT - weapon_height - 20

    if reloading:
        offset = (reload_timer % 20) - 10  # simple up/down animation
        y += offset

    pygame.draw.rect(screen, DARKGRAY, (x + 20, y + 60, 20, 40))  # handle
    pygame.draw.rect(screen, BLACK, (x + 25, y + 20, 10, 40))     # barrel
    pygame.draw.circle(screen, RED, (x + 30, y + 70), 4)  