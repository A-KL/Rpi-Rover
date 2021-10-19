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

    while start_x < SCREEN_WIDTH + 100:
        pygame.draw.lines(chevron_surface, color_a, False, ((start_x, start_y), (start_x + shift_x, start_y + shift_x)), width)
        start_x = start_x + width

        pygame.draw.lines(chevron_surface, color_b, False, ((start_x, start_y), (start_x+ shift_x, start_y + shift_x)), width)
        start_x = start_x + width
        
    return chevron_surface
        
if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 200
    DISPLAY = (SCREEN_WIDTH,SCREEN_HEIGHT)

    screen = pygame.display.set_mode(DISPLAY)	
    screen.fill(pygame.Color('#000000'))

    font = pygame.font.Font('/home/pi/projects/Rover/src/gui/whitrabt.ttf', 70)
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

