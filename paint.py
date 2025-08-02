import pygame
from pygame.locals import QUIT

pygame.init()
pygame.display.set_caption("Paint")

width, height = 800, 600
toolbar_height = 200

screen = pygame.display.set_mode((width, height))

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BROWN = (165, 42, 42)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
colors = [WHITE, BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, BROWN, PINK, ORANGE, GRAY]

#variables
drawing = False
brush_size = 5
min_brush_size = 2
max_brush_size = 50
brush_color = BLACK
eraser_mode = False
last_pos = None

#create a surface for the drawing area
canvas = pygame.Surface((width, height - toolbar_height))
canvas.fill(WHITE)

#create the toolbar
toolbar = pygame.Surface((width, toolbar_height))
toolbar.fill(GRAY)

running = True
while running:
    font = pygame.font.Font(None, 36)
    pen_text = font.render("Pen", True, BLACK)
    eraser_text = font.render("Eraser", True, BLACK)
    clear_text = font.render("Clear", True, BLACK)
    decrease_text = font.render("-", True, BLACK)
    increase_text = font.render("+", True, BLACK)

    toolbar.blit(pen_text, (10, 10))
    toolbar.blit(eraser_text, (10, 50))
    toolbar.blit(clear_text, (10, 90))
    toolbar.blit(decrease_text, (10, 130))
    toolbar.blit(increase_text, (10, 170))

pygame.display.flip()
pygame.quit()