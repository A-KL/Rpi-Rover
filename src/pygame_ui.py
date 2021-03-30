import os
import pygame
import pygame_gui
import pygame_gui_custom

if __name__ == "__main__":    
    # initialize the display
    pygame.init()
    pygame.font.init()

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

    is_running = True

    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()