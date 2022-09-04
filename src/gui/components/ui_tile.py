import pygame
from pygame import *

class UITileBackgroundStyle:

    def __init__(self, color: Color, footer_color: Color, footer_border_color: Color):
        self.color = color
        self.footer_color = footer_color
        self.footer_border_color = footer_border_color 

class UITileForegroundStyle:

    def __init__(self, font_path: str, color: Color, footer_color: Color, body_placeholder: str = "0", body_placeholder_size: int = 0):
        self.font_path = font_path
        self.color = color
        self.footer_color = footer_color
        self.body_place_holder = body_placeholder
        self.body_place_holder_size = body_placeholder_size

class UITileStyle:

    def __init__(self, background: UITileBackgroundStyle, foreground: UITileForegroundStyle):
        self.background = background
        self.foreground = foreground

class UITile:

    def __init__(self, width: int, height: int, caption: str, text: str, footer: str, style: UITileStyle):
        self.surface = Surface((width, height))
        self.caption = caption
        self.text = text
        self.footer = footer
        self.style = style
        self.rect = None

    def update(self):
        pygame_ui_draw_tile(self.surface, self.caption, self.text, self.footer, self.style.background, self.style.foreground)
        return self.surface

    def hit(self, position):
        if self.rect == None:
            return False
        return self.rect.collidepoint(position)

    def blit(self, screen: Surface, dest):
        self.rect = screen.blit(self.update(), dest)


def pygame_ui_draw_tile(surface: Surface, caption: str, text: str, footer: str, style: UITileBackgroundStyle, text_style: UITileForegroundStyle):    
    width = surface.get_width()
    height = surface.get_height()

    # Body
    body_height = height * 0.74
    footer_height = height - body_height

    pygame.draw.rect(surface, style.color, (0, 0, width, body_height))

    # Footer
    colors = [
        (0, style.footer_border_color), 
        (4, style.footer_color)
    ]

    for w, color in colors:
        pygame.draw.polygon(surface, color, (
                (0 + w-1, body_height + footer_height / 2),
                (0 + w-1, body_height + w),
                (width - w, body_height + w),
                (width - w, height - w),
                (footer_height / 2, height - w)))

    # Text

    font_big = pygame.font.Font(text_style.font_path, int(width / 6))
    font_small = pygame.font.Font(text_style.font_path, int(width / 11))

    caption_surface = font_small.render(caption, True, text_style.color)
    text_surface = font_big.render(text, True, text_style.color)
    footer_surface = font_small.render(footer, True, text_style.footer_color)

    padding = caption_surface.get_height() / 2

    value_len = len(text)
    h, s, v, a = style.color.hsva
    place_holder_color = Color(0)
    place_holder_color.hsva = (h, s, v * 0.75, a)

    left = text_style.body_place_holder_size - value_len
    if left > 0:
        for x in range(1, left + 1):
            place_holder_text = font_big.render(text_style.body_place_holder, True, place_holder_color)
            surface.blit(place_holder_text, (width - padding  - text_surface.get_width() - place_holder_text.get_width() * x, body_height - text_surface.get_height() - padding))

    surface.blit(caption_surface, (padding, padding))

    surface.blit(text_surface, (width - padding - text_surface.get_width(), body_height - text_surface.get_height() - padding))

    surface.blit(footer_surface, (width - padding - footer_surface.get_width(), (footer_height - footer_surface.get_height())/ 2 + body_height))