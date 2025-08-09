import pygame
from pygame.locals import QUIT

pygame.init()
pygame.display.set_caption("Paint")

WIDTH  = 400
HEIGHT = 300
toolbar_height = 50

#color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

# create the window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

#VARIABLES
drawing = False
brush_size = 5
min_brush_size = 2  
max_brush_size = 50
brush_color = BLACK
erase_mode = False
last_pos = None


# create a surface for drawing
canvas = pygame.Surface((WIDTH, HEIGHT - toolbar_height))
canvas.fill(WHITE)

# create the toolbar
toolbar = pygame.Surface((WIDTH, toolbar_height))
toolbar.fill(GREY)

running = True
while running:
    toolbar.fill(GREY)
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
                    if brush_size > min_brush_size:
                        brush_size -= 1
                        print(f"Brush size decreased to {brush_size}")
                elif increase_rect.collidepoint(event.pos):
                    if brush_size < max_brush_size:
                        brush_size += 1
                        print(f"Brush size increased to {brush_size}")
                elif black_button_color.collidepoint(event.pos):
                    brush_color = BLACK
                    print("Color changed to black")
                elif red_button_color.collidepoint(event.pos):
                    brush_color = RED
                    print("Color changed to red")

            else:
                drawing = True
                last_pos = (event.pos[0], event.pos[1] - toolbar_height)
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_pos = None
        elif event.type == pygame.MOUSEMOTION and drawing:
            color = brush_color if not erase_mode else WHITE
            pygame.draw.line(canvas, color, last_pos, (event.pos[0], event.pos[1] - toolbar_height), brush_size)
            last_pos = (event.pos[0], event.pos[1] - toolbar_height)




    pygame.display.flip()
pygame.quit






