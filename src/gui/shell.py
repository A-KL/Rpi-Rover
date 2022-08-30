import os
from os.path import join

import pygame
from pygame import *

from components.ui_tile import *
from components.ui_colors import *

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 480
    DISPLAY = (SCREEN_WIDTH,SCREEN_HEIGHT)

    screen = pygame.display.set_mode(DISPLAY)	
    screen.fill(pygame.Color('#000000'))

    current_dir = os.path.dirname(os.path.abspath(__file__))
    current_file = os.path.basename(__file__)
    font_path = join(current_dir, 'whitrabt.ttf')

    is_running = True

    DarkGrayTileStyle = UITileStyle(DarkGray, Black, DarkGray)
    DarkGrayTileTextStyle = UITileTextStyle(font_path, Black, DarkGray)

    LightGreenTileStyle = UITileStyle(LightGreen, Black, LightGreen)
    LightGreenTileTextStyle = UITileTextStyle(font_path, Black, LightGreen)

    tiles = [
        UITile(225, 150, "main_power", "0.95a", current_file, DarkGrayTileStyle, DarkGrayTileTextStyle),
        UITile(225, 150, "aux_power", "1.0a", current_file, DarkGrayTileStyle, DarkGrayTileTextStyle),
        UITile(225, 150, "state", "RUNNING", current_file, DarkGrayTileStyle, DarkGrayTileTextStyle)
    ]

    while is_running:

        map = []

        for index, tile in enumerate(tiles):
            tile_surface = tile.update()
            map.append(
                (tile,  screen.blit(tile_surface, (10 * (index + 1) + tile_surface.get_width() * index, 10)))
            )

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONUP:
                for tile, tile_rect in map:
                    if tile_rect.collidepoint(pygame.mouse.get_pos()):
                        if tile.background == DarkGrayTileStyle:
                            tile.background = LightGreenTileStyle
                            tile.foreground = LightGreenTileTextStyle
                        else:
                            tile.background = DarkGrayTileStyle
                            tile.foreground = DarkGrayTileTextStyle

            if event.type == pygame.QUIT or event.type == 1792:
                print(event)
                is_running = False
        
        pygame.display.update()    