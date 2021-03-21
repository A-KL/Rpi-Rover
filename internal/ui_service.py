import time
import logging
import argparse
import pygame
import pygame.freetype  # Import the freetype module.
import os
import sys
import numpy as np
import subprocess
import signal

# os.environ['SDL_FBDEV'] = "/dev/fb1"
# os.environ['SDL_VIDEODRIVER'] = "fbcon"

# os.environ["SDL_FBDEV"] = "/dev/fb0"
os.environ["SDL_VIDEODRIVER"] = "dummy"

if __name__ == "__main__":
    dir = os.path.dirname(os.path.abspath(__file__))

    # load 
    # warning1 = pygame.image.load(os.path.join(dir, 'warning.png'))
    # danger = pygame.image.load(os.path.join(dir, 'klaudio-ladavac-warning-holoanimation-1c.gif'))
    # warning = pygame.image.load(os.path.join(dir, 'klaudio-ladavac-warning-holoanimation-2b.gif'))

    # initialize the display
    pygame.init()
    screen = pygame.display.set_mode((1,1))
    # screen = pygame.display.set_mode((320, 240)) #pygame.FULLSCREEN
    screen.fill((0,0,0))

    main_font = pygame.font.Font('/home/pi/projects/Rover/assets/fonts/whitrabt.ttf', 18)
    main_color = (255, 0, 56)

    buffer = pygame.Surface((screen.get_width(), screen.get_height()))

    # buffer.blit(danger, ((screen.get_width() / 2) - (danger.get_width() / 2),
    #                 (screen.get_height() / 2) - (danger.get_height() / 2)))

    font_surface = main_font.render("Loading...", True, main_color)
    buffer.blit(font_surface, (30, 180))

    pygame.draw.line(buffer, main_color, (30, 210), (screen.get_width()-30, 210), 2)

    print(screen.get_rect())

    screen.blit(buffer, (0,0))
    pygame.display.update()

    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()