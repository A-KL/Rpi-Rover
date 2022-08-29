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

class TileUI:

    def __init__(self, width, height, title, value, footer, font_path, pimary_color = DarkGray, background_color = Black):
        self.surface = Surface((width, height))
        self.title = title
        self.value = value
        self.footer = footer
        self.font_path = font_path
        self.pimary_color = pimary_color
        self.background_color = background_color
        self.value_place_holder = "0"
        self.value_place_holder_size = 0

    def update(self):
        # Background
        width = self.surface.get_width()
        height = self.surface.get_height()
        body_height = height * 0.74
        footer_height = height - body_height

        pygame.draw.rect(self.surface, self.pimary_color, (0, 0, width, body_height))

        pygame.draw.rect(self.surface, self.background_color, (0, 0 + body_height, width, footer_height))

        colors = [self.pimary_color, self.background_color]
        color_index = 0

        for w in [0, 7]:
            pygame.draw.polygon(self.surface, colors[color_index], (
                    (0 + w, body_height + footer_height / 2),
                    (0 + w, body_height + w),
                    (width - w, body_height + w),
                    (width - w, height - w),
                    (footer_height / 2, height - w)
                )
            )
            color_index += 1

        # Text

        font_big = pygame.font.Font(self.font_path, int(width / 7))
        font_small = pygame.font.Font(self.font_path, int(width / 14))

        title_text = font_small.render(self.title, True, self.background_color)
        main_text = font_big.render(self.value, True, self.background_color)
        footer_text = font_small.render(self.footer, True, self.pimary_color)

        padding = title_text.get_height()

        value_len = len(self.value)
        h, s, v, a = self.pimary_color.hsva
        place_holder_color = Color(0)
        place_holder_color.hsva = (h, s, v * 0.75, a)

        left = self.value_place_holder_size - value_len
        if left > 0:
            for x in range(1, left + 1):
                place_holder_text = font_big.render(self.value_place_holder, True, place_holder_color)
                self.surface.blit(place_holder_text, (width - padding  - main_text.get_width() - place_holder_text.get_width() * x, body_height - main_text.get_height() - padding))

        self.surface.blit(title_text, (padding, padding))

        self.surface.blit(main_text, (width - padding - main_text.get_width(), body_height - main_text.get_height() - padding))

        self.surface.blit(footer_text, (width - padding - footer_text.get_width(), (footer_height - footer_text.get_height())/ 2 + body_height))

        return self.surface

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

    is_running = True

    tiles = [
        TileUI(225, 150, "main_power", "0.95a", current_file, join(current_dir, 'whitrabt.ttf')),
        TileUI(225, 150, "aux_power", "1.0a", current_file, join(current_dir, 'whitrabt.ttf')),
        TileUI(225, 150, "state", "RUNNING", current_file, join(current_dir, 'whitrabt.ttf'))
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
                        if tile.pimary_color == LightGreen:
                            tile.pimary_color = DarkGray
                        else:
                            tile.pimary_color = LightGreen

            if event.type == pygame.QUIT or event.type == 1792:
                print(event)
                is_running = False
        
        pygame.display.update()    