import pygame

class UIGridLayout:
    def __init__(self, 
                relative_rect: pygame.Rect,
                rows : int,
                columns : int,
                margin : int):
        self.rows = rows
        self.columns = columns
        self.margin = margin
        self.parent = relative_rect

    def get(self, row: int, col: int):

        tile_w = self.parent.width / self.columns
        tile_h = self.parent.height / self.rows

        x = self.margin + col * tile_w
        y = self.margin + row * tile_h
        w = tile_w - self.margin * 2
        h = tile_h - self.margin * 2

        return pygame.Rect(x, y, w, h)