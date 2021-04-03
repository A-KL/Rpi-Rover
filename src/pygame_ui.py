import os
import pygame
import pygame_gui
import pygame_gui_custom

if __name__ == "__main__":    
    # initialize the display
    pygame.init()
    pygame.font.init()

    pygame.mouse.set_visible(False)

    dir = os.path.dirname(os.path.abspath(__file__))

    window_surface = pygame.display.set_mode((800, 480))
    manager = pygame_gui.UIManager((800, 480))
    clock = pygame.time.Clock()
    background = pygame.Surface((800, 480))

    logic_v = pygame_gui_custom.UIStack(pygame.Rect(10, 10, 200, 80), 2, manager)
    logic_v.tmp_init(0, 6, 5.14, 'V', 'logic')

    logic_i = pygame_gui_custom.UIStack(pygame.Rect(220, 10, 200, 80), 2, manager)
    logic_i.tmp_init(0, 4, 2.14, 'I', 'logic')

    main_v = pygame_gui_custom.UIStack(pygame.Rect(10, 100, 200, 80), 2, manager)
    main_v.tmp_init(0, 16, 11.01, 'V', 'main')

    main_i = pygame_gui_custom.UIStack(pygame.Rect(220, 100, 200, 80), 2, manager)
    main_i.tmp_init(0, 4, 1.04, 'I', 'main')

    # print(pygame.image.get_extended())

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

        window_surface.blit(background, (0, 0))
        # manager.draw_ui(window_surface)
        window_surface.blit(hal_outer_sprite, (200, 40))

        window_surface.blit(hal_inner_sprite, (x, y))

        if alpha < 0 or alpha >= 256:
            step = step * -1

        alpha += step 

        hal_inner_sprite.set_alpha(alpha)

        pygame.display.update()