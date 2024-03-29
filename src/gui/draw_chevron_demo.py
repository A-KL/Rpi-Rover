import os
from os.path import join

import pygame
from pygame import *

from components.ui_chevron import *
        
if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 200
    DISPLAY = (SCREEN_WIDTH,SCREEN_HEIGHT)

    screen = pygame.display.set_mode(DISPLAY)	
    screen.fill(pygame.Color('#000000'))

    current_path = os.path.dirname(os.path.abspath(__file__))
    font = pygame.font.Font(join(current_path, 'whitrabt.ttf'), 70)
    font_color = (255, 0, 56)

    text0 = font.render("Error!", True, font_color)

    chevron_top_surface = draw_chevron(SCREEN_WIDTH, SCREEN_HEIGHT, 20, font_color)
    chevron_bottom_surface = draw_chevron(SCREEN_WIDTH, SCREEN_HEIGHT, 20, font_color)

    is_running = True

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == 1792:
                print(event)
                is_running = False
            
        screen.blit(chevron_top_surface, (-20, 0))
        screen.blit(chevron_bottom_surface, (-20, SCREEN_HEIGHT - 40))
        screen.blit(text0, (10, 70))
        
        pygame.display.update()

