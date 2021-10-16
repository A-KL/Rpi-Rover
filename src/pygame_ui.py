import os
import cv2
import pygame
import pygame_gui
import pygame_gui.elements

from gui.UIStack import *
from gui.GridLayout import *
from gui.ui_helpers import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
SCREEN_POSITION = (0,0)
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

MESSAGE_WIDTH = 700
MESSAGE_HEIGHT = 380
MESSAGE_SIZE = (MESSAGE_WIDTH, MESSAGE_HEIGHT)
MESSAGE_POSITION = ( (SCREEN_WIDTH - MESSAGE_WIDTH) / 2, (SCREEN_HEIGHT - MESSAGE_HEIGHT) / 2)

def draw_chevron(screen_width, screen_height, thickness = 15, color = Color("Red")):
    chevron_surface = Surface((screen_width + thickness *2, screen_height))
    
    start_x = 0
    start_y = 0
    width = thickness
    shift_x = width * 2

    color_a = color
    color_b = Color("Black")

    while start_x < screen_width + 100:
        pygame.draw.lines(chevron_surface, color_a, False, ((start_x, start_y), (start_x + shift_x, start_y + shift_x)), width)
        start_x = start_x + width

        pygame.draw.lines(chevron_surface, color_b, False, ((start_x, start_y), (start_x+ shift_x, start_y + shift_x)), width)
        start_x = start_x + width
        
    return chevron_surface

def draw_message_box(surface: pygame.Surface, font: pygame.font.Font, message, description, color):
    caption = font.render(message, True, color)

    chevron_top_surface = draw_chevron(MESSAGE_WIDTH, MESSAGE_HEIGHT, 20, color)
    chevron_bottom_surface = draw_chevron(MESSAGE_WIDTH, MESSAGE_HEIGHT, 20, color)

    surface.blit(chevron_top_surface, (-20, 4))
    surface.blit(chevron_bottom_surface, (-20, MESSAGE_HEIGHT - 40 - 4))
    surface.blit(caption, (10, 70))
    surface.blit(description, (10, 120))

    pygame.draw.rect(surface, color, ((0,0), MESSAGE_SIZE), 1),

def draw_next_frame(surface: pygame.Surface, cap: cv2.VideoCapture, position :Tuple[float, float] , alpha :int):
    success, img = cap.read()

    if success:
        shape = img.shape[1::-1]
        frame = pygame.image.frombuffer(img.tobytes(), shape, "BGR")
        frame.set_alpha(alpha)
        surface.blit(frame, position)
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

if __name__ == "__main__":    
    PRIMARY_COLOR = (255, 0, 56)
    GREEN_COLOR = (0, 255, 0)
    YELLOW_COLOR = (255, 204, 0)

    pygame.init()
    pygame.font.init()
    pygame.mouse.set_visible(False)

    root = os.path.dirname(os.path.abspath(__file__))
    screen = pygame.display.set_mode(SCREEN_SIZE)
    manager = pygame_gui.UIManager(SCREEN_SIZE, root + '/gui/base_theme.json')
    clock = pygame.time.Clock()

    display_surface = pygame.Surface(SCREEN_SIZE)
    message_surface = pygame.Surface(MESSAGE_SIZE)

    whitrabt_70 = pygame.font.Font(root + '/../assets/fonts/whitrabt.ttf', 70)
    whitrabt_20 = pygame.font.Font(root + '/../assets/fonts/whitrabt.ttf', 20)
    oblivious_70 = pygame.font.Font(root + '/../assets/fonts/ObliviousFont.ttf', 70)

    layout = GridLayout(pygame.Rect(SCREEN_POSITION, SCREEN_SIZE), 5, 4, 5)

    # ============================================================= 
    cap = cv2.VideoCapture(root + '/../assets/img/Old TV Static.mp4')
    if not cap.isOpened():
        raise NameError('Can not open background video file.')
    
    background_image = pygame.image.load(root + '/../assets/img/background.bmp')
    background_image.convert()
    background_image.set_alpha(80)

    display_surface.blit(background_image, SCREEN_POSITION)
    # =============================================================

    logic_v = UIStack(layout.get(2, 0), 2, manager) # 200 / 80
    logic_v.tmp_init(0, 6, 5.14, 'V', 'logic')

    logic_i = UIStack(layout.get(2, 1), 2, manager)
    logic_i.tmp_init(0, 4, 2.14, 'I', 'logic')

    main_v = UIStack(layout.get(2, 2), 2, manager)
    main_v.tmp_init(0, 16, 11.01, 'V', 'main')

    main_i = UIStack(layout.get(2, 3), 2, manager)
    main_i.tmp_init(0, 4, 1.04, 'I', 'main')

    # =============================================================

    close_button = pygame_gui.elements.UIButton(layout.get(3, 3), "Close", manager)
    show_button = pygame_gui.elements.UIButton(layout.get(3, 2), "Show", manager)

    # =============================================================

    error_text = whitrabt_70.render("Error.", True, PRIMARY_COLOR)
    warning_text = whitrabt_70.render("Warning.", True, YELLOW_COLOR)
    success_text = oblivious_70.render("Success.", True, GREEN_COLOR)

    message_color = GREEN_COLOR

    chevron_top_surface = draw_chevron(MESSAGE_WIDTH, MESSAGE_HEIGHT, 20, message_color)
    chevron_bottom_surface = draw_chevron(MESSAGE_WIDTH, MESSAGE_HEIGHT, 20, message_color)

    message_surface.blit(chevron_top_surface, (-20, 4))
    message_surface.blit(chevron_bottom_surface, (-20, MESSAGE_HEIGHT - 40 - 4))
    message_surface.blit(success_text, (10, 70))

    pygame.draw.rect(message_surface, message_color, ((0,0), MESSAGE_SIZE), 1),

    # =============================================================

    # hal_outer_sprite = pygame.image.load(root + '/../assets/img/1280px-HAL9000-outer.bmp')
    # hal_outer_sprite.convert()

    # hal_outer_sprite = pygame.transform.rotate(hal_outer_sprite, -90)
    # hal_outer_sprite = pygame.transform.smoothscale(hal_outer_sprite, (400, 400))

    # hal_inner_sprite = pygame.image.load(root + '/../assets/img/1280px-HAL9000-inner.bmp')
    # hal_inner_sprite.convert()

    # hal_inner_sprite = pygame.transform.rotate(hal_inner_sprite, -90)
    # w = int(908/3)
    # h = int(860/3)
    # x = int((800 - w ) / 2)
    # y = int((480 - h ) / 2)
    # hal_inner_sprite = pygame.transform.smoothscale(hal_inner_sprite, (w, h))

    # alpha = 0
    # step = 15

# =============================================================

    is_running = True
    show_message = True

    while is_running:
        time_delta = clock.tick(60)/1000.0
        
        for event in pygame.event.get():
            if event.type == 1792 and show_message:
                show_message = False

            if event.type == pygame.QUIT:
                is_running = False

            manager.process_events(event)

        draw_next_frame(display_surface, cap, SCREEN_POSITION, 40)

        screen.blit(display_surface, SCREEN_POSITION)

        if close_button.check_pressed():
            is_running = False

        if show_button.check_pressed():
            show_message = True

        manager.update(time_delta)

        manager.draw_ui(screen)

        if show_message:
            screen.blit(message_surface, MESSAGE_POSITION)

        # window_surface.blit(hal_outer_sprite, (200, 40))
        # window_surface.blit(hal_inner_sprite, (x, y))

        # if alpha < 0 or alpha >= 256:
        #     step = step * -1

        # alpha += step 

        # hal_inner_sprite.set_alpha(alpha)

        pygame.display.update()