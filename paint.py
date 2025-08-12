import pygame
from pygame.locals import QUIT

pygame.init()
pygame.display.set_caption("Paint")

WIDTH  = 800
HEIGHT = 600
toolbar_height = 50

#color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# create the window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

#VARIABLES
drawing = False
brush_size = 5
eraser_size = 5
min_brush_size = 2
max_brush_size = 50
min_erase_size = 2
max_erase_size = 50
brush_color = BLACK
erase_mode = False
last_pos = None


# create a surface for drawing
canvas = pygame.Surface((WIDTH, HEIGHT - toolbar_height))
canvas.fill(WHITE)

# create the toolbar
toolbar = pygame.Surface((WIDTH, toolbar_height))
toolbar.fill(WHITE)


running = True
while running:
    toolbar.fill(WHITE)
    pygame.draw.rect(toolbar, BLACK, toolbar.get_rect(), 2)
    font = pygame.font.SysFont(None, 24)
    pen_text = font.render("P", True, BLACK)
    erase_text = font.render("E", True, BLACK)
    clear_text = font.render("C", True, BLACK)
    decrease_text = font.render("-", True, BLACK)   
    incerease_text = font.render("+", True, BLACK)

    toolbar.blit(pen_text, (40, 20))
    toolbar.blit(erase_text, (80, 20))  
    toolbar.blit(clear_text, (120, 20))
    toolbar.blit(decrease_text, (160, 20))  
    toolbar.blit(incerease_text, (200, 20))

    # draw the color selection buttons
    color_button_width = 20
    color_button_height = 20
    black_button_color = pygame.draw.circle(toolbar, BLACK, (240, 25), color_button_width // 2)
    red_button_color = pygame.draw.circle(toolbar, RED, (280, 25), color_button_width // 2)
    green_button_color = pygame.draw.circle(toolbar, GREEN, (320, 25), color_button_width // 2)
    blue_button_color = pygame.draw.circle(toolbar, BLUE, (360, 25), color_button_width // 2)
    grey_button_color = pygame.draw.circle(toolbar, GREY, (400, 25), color_button_width // 2)
    yellow_button_color = pygame.draw.circle(toolbar, YELLOW, (440, 25), color_button_width // 2)
    pink_button_color = pygame.draw.circle(toolbar, PINK, (480, 25), color_button_width // 2)
    purple_button_color = pygame.draw.circle(toolbar, PURPLE, (520, 25), color_button_width // 2)
    orange_button_color = pygame.draw.circle(toolbar, ORANGE, (560, 25), color_button_width // 2)

    WINDOW.fill(WHITE)
    WINDOW.blit(canvas, (0, toolbar_height))
    WINDOW.blit(toolbar, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1]  <= toolbar_height:
                pen_rect = pen_text.get_rect(topleft=(40, 20))
                erase_rect = erase_text.get_rect(topleft=(80, 20))
                clear_rect = clear_text.get_rect(topleft=(120, 20))
                decrease_rect = decrease_text.get_rect(topleft=(160, 20))
                increase_rect = incerease_text.get_rect(topleft=(200, 20))

                if pen_rect.collidepoint(event.pos):
                    erase_mode = False
                    print("Pen mode activated")
                elif erase_rect.collidepoint(event.pos):
                    erase_mode = True
                    print("Erase mode activated")
                elif clear_rect.collidepoint(event.pos):
                    canvas.fill(WHITE)
                    print("Canvas is cleared")
                elif decrease_rect.collidepoint(event.pos):
                    if brush_size > min_brush_size and erase_mode == False:
                        brush_size -= 1
                        print(f"Brush size decreased to {brush_size}")
                    else:
                        eraser_size -= 1
                        print(f"Eraser size decreased to {eraser_size}")
                elif increase_rect.collidepoint(event.pos):
                    if brush_size < max_brush_size and erase_mode == False:
                        brush_size += 1
                        print(f"Brush size increased to {brush_size}")
                    else:
                        eraser_size += 1
                        print(f"Eraser size increased to {eraser_size}")
                elif black_button_color.collidepoint(event.pos):
                    brush_color = BLACK
                    print("Color changed to black")
                elif red_button_color.collidepoint(event.pos):
                    brush_color = RED
                    print("Color changed to red")
                elif green_button_color.collidepoint(event.pos):
                    brush_color = GREEN
                    print("Color changed to green")
                elif blue_button_color.collidepoint(event.pos):
                    brush_color = BLUE
                    print("Color changed to blue")
                elif grey_button_color.collidepoint(event.pos):
                    brush_color = GREY
                    print("Color changed to grey")
                elif yellow_button_color.collidepoint(event.pos):
                    brush_color = YELLOW
                    print("Color changed to yellow")
                elif pink_button_color.collidepoint(event.pos):
                    brush_color = PINK
                    print("Color changed to pink")
                elif purple_button_color.collidepoint(event.pos):
                    brush_color = PURPLE
                    print("Color changed to purple")
                elif orange_button_color.collidepoint(event.pos):
                    brush_color = ORANGE
                    print("Color changed to orange")
            else:
                drawing = True
                last_pos = (event.pos[0], event.pos[1] - toolbar_height)
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_pos = None
        elif event.type == pygame.MOUSEMOTION and drawing:
            color = brush_color if not erase_mode else WHITE
            size = brush_size if not erase_mode else eraser_size
            pygame.draw.line(canvas, color, last_pos, (event.pos[0], event.pos[1] - toolbar_height), size)
            last_pos = (event.pos[0], event.pos[1] - toolbar_height)




    pygame.display.flip()
pygame.quit






