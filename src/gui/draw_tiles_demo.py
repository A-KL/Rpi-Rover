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

    LightYellowTileStyle = UITileStyle(LightYellow, Black, LightYellow)
    LightYellowTileTextStyle = UITileTextStyle(font_path, Black, LightYellow)

    LightRedTileStyle = UITileStyle(LightRed, Black, LightRed)
    LightRedTileTextStyle = UITileTextStyle(font_path, Black, LightRed)

    SolidLightRedTileStyle = UITileStyle(DarkGray, LightRed, LightRed)
    SolidLightRedTileTextStyle = UITileTextStyle(font_path, LightRed, Black)

    tiles = [
        UITile(185, 120, "main_power", "0.95a", current_file, DarkGrayTileStyle, DarkGrayTileTextStyle),
        UITile(185, 120, "12/08/2023", "1.0a", current_file, SolidLightRedTileStyle, SolidLightRedTileTextStyle),
        UITile(185, 120, "state", "RUNNING", current_file, LightRedTileStyle, LightRedTileTextStyle),

        UITile(185, 120, "main_power", "0.95a", current_file, DarkGrayTileStyle, DarkGrayTileTextStyle),
        UITile(185, 120, "aux_power", "1.0a", current_file, LightYellowTileStyle, LightYellowTileTextStyle),
        UITile(185, 120, "192.168.1.1", "STOP", current_file, DarkGrayTileStyle, DarkGrayTileTextStyle)      
    ]

    columns = 4
    rows = 2
    padding = 12

    while is_running:

      for y in range(0, rows):
        for x in range(0, columns):
            index = y * columns + x
            if index>= len(tiles):
                continue
            tile = tiles[index]
            tile.blit(screen, 
                (
                    padding * (x + 1) + tile.surface.get_width() * x,
                    padding * (y + 1) + tile.surface.get_height() * y
                )
            )

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONUP:
                for tile in tiles:
                    if tile.rect.collidepoint(pygame.mouse.get_pos()):
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