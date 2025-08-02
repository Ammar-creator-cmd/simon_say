import pygame
import sys
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Set up display
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python FPS")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)



# Crosshair
crosshair = pygame.Surface((20, 20), pygame.SRCALPHA)
pygame.draw.circle(crosshair, RED, (10, 10), 10, 2)

# Enemy
enemy_size = 50

def spawn_enemy():
    x = random.randint(enemy_size, WIDTH - enemy_size)
    y = random.randint(enemy_size, HEIGHT - enemy_size)
    return pygame.Rect(x, y, enemy_size, enemy_size)

# Game variables
score = 0
health = 5
ammo = 10
enemy = spawn_enemy()
font = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(60)
    window.fill(BLACK)

    # Draw enemy
    pygame.draw.rect(window, GREEN, enemy)

    # Draw crosshair
    mouse_x, mouse_y = pygame.mouse.get_pos()
    window.blit(crosshair, (mouse_x - 10, mouse_y - 10))

    # Draw HUD
    score_text = font.render(f"Score: {score}", True, WHITE)
    health_text = font.render(f"Health: {health}", True, RED)
    ammo_text = font.render(f"Ammo: {ammo}", True, WHITE)
    reload_text = font.render("Press R to Reload", True, WHITE)

    window.blit(score_text, (20, 20))
    window.blit(health_text, (20, 60))
    window.blit(ammo_text, (WIDTH - 160, 20))
    window.blit(reload_text, (WIDTH - 220, 60))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Shooting
        if event.type == pygame.MOUSEBUTTONDOWN and ammo > 0:
            shoot_sound.play()
            ammo -= 1
            if enemy.collidepoint(mouse_x, mouse_y):
                hit_sound.play()
                score += 1
                enemy = spawn_enemy()
            else:
                health -= 1
                if health <= 0:
                    running = False

        # Reload
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                ammo = 10

    pygame.display.flip()

pygame.quit()
sys.exit()
