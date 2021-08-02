import os
import pygame
import pygame_gui
from gui.dashboard import *
from gui.ui_helpers import *

if __name__ == "__main__":    
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 480
    DISPLAY = (SCREEN_WIDTH,SCREEN_HEIGHT)
    PRIMARY_COLOR = (255, 0, 56)
    GREEN_COLOR = (0, 255, 0)
    YELLOW_COLOR = (255, 204, 0)

    dir = os.path.dirname(os.path.abspath(__file__))

    pygame.init()
    pygame.font.init()

    pygame.mouse.set_visible(False)

    screen = pygame.display.set_mode(DISPLAY)
    manager = pygame_gui.UIManager(DISPLAY)
    clock = pygame.time.Clock()
    background = pygame.Surface(DISPLAY)

    whitrabt = pygame.font.Font(dir + '/gui/whitrabt.ttf', 70)
    oblivious = pygame.font.Font(dir + '/gui/ObliviousFont.ttf', 70)

    # =============================================================

    logic_v = UIStack(pygame.Rect(10, 10, 200, 80), 2, manager)
    logic_v.tmp_init(0, 6, 5.14, 'V', 'logic')

    logic_i = UIStack(pygame.Rect(220, 10, 200, 80), 2, manager)
    logic_i.tmp_init(0, 4, 2.14, 'I', 'logic')

    main_v = UIStack(pygame.Rect(10, 100, 200, 80), 2, manager)
    main_v.tmp_init(0, 16, 11.01, 'V', 'main')

    main_i = UIStack(pygame.Rect(220, 100, 200, 80), 2, manager)
    main_i.tmp_init(0, 4, 1.04, 'I', 'main')

    # print(pygame.image.get_extended())

    # =============================================================

    error_text = whitrabt.render("Error.", True, PRIMARY_COLOR)
    warning_text = whitrabt.render("Warning.", True, YELLOW_COLOR)
    success_text = whitrabt.render("Success.", True, GREEN_COLOR)

    chevron_top_surface = draw_chevron(SCREEN_WIDTH, SCREEN_HEIGHT, 20, YELLOW_COLOR)
    chevron_bottom_surface = draw_chevron(SCREEN_WIDTH, SCREEN_HEIGHT, 20, YELLOW_COLOR)

    # =============================================================

    hal_outer_sprite = pygame.image.load(dir + '/../assets/img/1280px-HAL9000-outer.bmp')
    hal_outer_sprite.convert()

    hal_outer_sprite = pygame.transform.rotate(hal_outer_sprite, -90)
    hal_outer_sprite = pygame.transform.smoothscale(hal_outer_sprite, (400, 400))

    hal_inner_sprite = pygame.image.load(dir + '/../assets/img/1280px-HAL9000-inner.bmp')
    hal_inner_sprite.convert()

    hal_inner_sprite = pygame.transform.rotate(hal_inner_sprite, -90)
    w = int(908/3)
    h = int(860/3)
    x = int((800 - w ) / 2)
    y = int((480 - h ) / 2)
    hal_inner_sprite = pygame.transform.smoothscale(hal_inner_sprite, (w, h))

    is_running = True

    alpha = 0
    step = 15

    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            manager.process_events(event)

        manager.update(time_delta)

        #screen.blit(background, (0, 0))

        screen.blit(chevron_top_surface, (-20, 0))
        screen.blit(chevron_bottom_surface, (-20, SCREEN_HEIGHT - 40))
        screen.blit(warning_text, (10, 70))

        # manager.draw_ui(screen)

        # window_surface.blit(hal_outer_sprite, (200, 40))
        # window_surface.blit(hal_inner_sprite, (x, y))

        # if alpha < 0 or alpha >= 256:
        #     step = step * -1

        # alpha += step 

        # hal_inner_sprite.set_alpha(alpha)

        pygame.display.update()