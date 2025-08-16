import pygame
import sys
import random

pygame.init()

#set up the display
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('simon says')

# Ensure the mixer is initialized before loading sounds
if not pygame.mixer.get_init():
    pygame.mixer.init()

def safe_load_image(path, size):
    try:
        return pygame.transform.scale(pygame.image.load(path), size)
    except pygame.error:
        # Return a blank surface if image not found
        return pygame.Surface(size)

def safe_load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        # Return a dummy Sound object if sound not found
        class DummySound:
            def play(self): pass
        return DummySound()

superheroes = {
    1: {
        "image": safe_load_image('batman.png', (100, 100)),
        "sound": safe_load_sound('batman.wav')
    },
    2: {
        "image": safe_load_image('superman.png', (100, 100)),
        "sound": safe_load_sound('superman.wav')
    },
    3: {
        "image": safe_load_image('spiderman.png', (100, 100)),
        "sound": safe_load_sound('spiderman.wav')
    },
    4: {
        "image": safe_load_image('ironman.png', (100, 100)),
        "sound": safe_load_sound('ironman.wav')
    }
}

#superheroes[1]["sound"].play()
#pygame.time.delay(1000)

sequence = []

def display_message(message, color = (255, 255, 255)):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
    window.blit(text, text_rect)
    pygame.display.update()

def display_image():
    for i in range(1,5):
        window.blit(superheroes[i]["image"], (i * 150, window_height // 2 - 50))
    pygame.display.update()

def play_sequence(length):
    global sequence
    sequence = [random.randint(1, 4) for _ in range(length)]
    display_message("Listen carefully!", (255, 0, 0))
    pygame.time.delay(2000)

    for superhero in sequence:
        superheroes[superhero]["sound"].play()
        display_image()
        pygame.time.delay(1000)
      


#play_sequence(10)

#function to play the sequence and get player input
def play_sequence_and_get_input():
    global sequence
    sequence_length = len(sequence) + 1
    play_sequence(sequence_length)

    #wait for player input
    for i, superheroes in enumerate(sequence):
        waiting_for_input = True
        start_time = pygame.time.get_ticks() #start new timer``
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Check if the mouse click is on the superhero image
                    image_rect = superheroes[superheroes]["image"].get_rect()
                    image_rect.topleft = ((superheroes - 1) * 100 + 25, 100)

                    if image_rect.collidepoint(mouse_x, mouse_y):
                        superheroes[superheroes]["sound"].play()
                        display_image()
                        pygame.time.delay(1000)
                        waiting_for_input = False
                    else:
                        return False  # Player clicked wrong image
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit
    return True #correct input, continue the game

pygame.mixer.init()

game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #play sound
    if play_sequence_and_get_input():
        display_message("Correct! Next round...", (0, 255, 0))
        pygame.time.delay(2000)
    else:
        display_message("Wrong! Game Over!", (255, 0, 0))
        pygame.time.delay(2000)
        game_over = True

pygame.quit()
sys.exit()