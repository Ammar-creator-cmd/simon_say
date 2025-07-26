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
      


play_sequence(4)