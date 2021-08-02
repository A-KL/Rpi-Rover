import pygame
from pygame import *

def draw_chevron(screen_width, screen_height, thickness = 15, color = Color("Red")):
    chevron_surface = Surface((screen_width + thickness *2, screen_height))
    
    start_x = 0
    start_y = 0
    width = thickness
    shift_x = width * 2

    color_a = color
    color_b = Color("Black")

    while start_x < screen_width + 100:
        pygame.draw.lines(chevron_surface, color_a, False, ((start_x, start_y), (start_x + shift_x, start_y + shift_x)), width)
        start_x = start_x + width

        pygame.draw.lines(chevron_surface, color_b, False, ((start_x, start_y), (start_x+ shift_x, start_y + shift_x)), width)
        start_x = start_x + width
        
    return chevron_surface