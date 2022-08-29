import os
from os.path import join

import pygame
from pygame import *

LightGreen = Color(0, 255, 127)
LightOrange = Color(255, 127, 0)
LightBlue = Color(0, 127, 255)
LightRed = Color(255, 0, 127)
LightYellow = Color(255, 255, 0)

Black = Color(0, 0, 0)
DarkGray = Color(30, 30, 30)

def draw_tile(surface, title, value, footer, font_path, pimary_color = LightGreen, background_color = Black):
    
    # Background
    width = surface.get_width()
    height = surface.get_height()
    body_height = height * 0.74
    footer_height = height - body_height

    pygame.draw.rect(surface, pimary_color, (0, 0, width, body_height))

    pygame.draw.rect(surface, background_color, (0, 0 + body_height, width, footer_height))

    colors = [pimary_color, background_color]
    color_index = 0

    for w in [0, 7]:
        pygame.draw.polygon(surface, colors[color_index], (
                (0 + w, body_height + footer_height / 2),
                (0 + w, body_height + w),
                (width - w, body_height + w),
                (width - w, height - w),
                (footer_height / 2, height - w)
            )
        )
        color_index += 1

    # Text

    font_big = pygame.font.Font(font_path, 60)
    font_small = pygame.font.Font(font_path, 34)

    title_text = font_small.render(title, True, background_color)
    main_text = font_big.render(value, True, background_color)
    footer_text = font_small.render(footer, True, pimary_color)

    padding = title_text.get_height()

    value_len = len(value)
    place_holder_size = 8
    place_holder = "0"
    h, s, v, a = pimary_color.hsva
    place_holder_color = Color(0)
    place_holder_color.hsva = (h, s, v * 0.75, a)

    left = place_holder_size - value_len
    if left > 0:
        for x in range(1, left + 1):
            place_holder_text = font_big.render(place_holder, True, place_holder_color)
            surface.blit(place_holder_text, (width - padding  - main_text.get_width() - place_holder_text.get_width() * x, body_height - main_text.get_height() - padding))

    surface.blit(title_text, (padding, padding))

    surface.blit(main_text, (width - padding - main_text.get_width(), body_height - main_text.get_height() - padding))

    surface.blit(footer_text, (width - padding - footer_text.get_width(), (footer_height - footer_text.get_height())/ 2 + body_height))

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 480
    DISPLAY = (SCREEN_WIDTH,SCREEN_HEIGHT)

    screen = pygame.display.set_mode(DISPLAY)	
    screen.fill(pygame.Color('#000000'))

    current_dir = os.path.dirname(os.path.abspath(__file__))

    is_running = True

    tile_surface = Surface((450, 300))
    tile_color = LightYellow

    while is_running:
        draw_tile(tile_surface, "main_power", "0.95a", "current_sensor.py", join(current_dir, 'whitrabt.ttf'), tile_color)

        tile_rect = screen.blit(tile_surface, (10, 10))

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONUP:
                if tile_rect.collidepoint(pygame.mouse.get_pos()):
                    if tile_color == LightGreen:
                        tile_color = DarkGray
                    else:
                        tile_color = LightGreen

            if event.type == pygame.QUIT or event.type == 1792:
                print(event)
                is_running = False
        
        pygame.display.update()    