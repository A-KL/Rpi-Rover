from typing import Union, Dict, Tuple
import os
import pygame

from pygame_gui.core import ObjectID
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.core.interfaces import IContainerLikeInterface, IUIContainerInterface

from pygame_gui.core import UIElement, UIContainer
from pygame_gui.core.drawable_shapes import RectDrawableShape, RoundedRectangleShape

from pygame_gui.elements import UIPanel

class UIStack(UIPanel):
    def __init__(self, 
                 relative_rect: pygame.Rect,
                 starting_layer_height: int,
                 manager: IUIManagerInterface,
                 *,
                 element_id: str = 'stack',
                 margins: Dict[str, int] = None,
                 container: Union[IContainerLikeInterface, None] = None,
                 parent_element: UIElement = None,
                 object_id: Union[ObjectID, str, None] = None,
                 anchors: Dict[str, str] = None,
                 visible: int = 1
                 ):

        super().__init__(relative_rect=relative_rect,
                         starting_layer_height=starting_layer_height,
                         manager=manager,
                         element_id=element_id,
                         margins=margins,
                         container=container,
                         parent_element=parent_element,
                         object_id=object_id,
                         anchors=anchors,
                         visible=visible)

        self._create_valid_ids(container=container,
                               parent_element=parent_element,
                               object_id=object_id,
                               element_id=element_id)
        
        self.decoration_colour = "#FF0038"
        
        
        # self.background_colour = None
        # self.border_colour = None
        # self.background_image = None
        # self.border_width = 1
        # self.shadow_width = 2
        # self.shape_corner_radius = 0
        # self.shape = 'rectangle'

        # self.rebuild_from_changed_theme_data()
        
        # Temp
        self.font = 'whitrabt.ttf'
        self.min = 0
        self.max = 100
        self.value = 100
        self.units = 'v'
        self.hint = 'hint' 
    
    def tmp_init(self, min=0, max=100, value = 0, units=None, hint = None):
        self.min = min
        self.max = max
        self.value = value
        self.units = units
        self.hint = hint
    
    def update_value(self, value):
        self.value = value
    
    def update(self, time_delta: float):
        """
        A method called every update cycle of our application. Designed to be overridden by derived
        classes but also has a little functionality to make sure the panel's layer 'thickness' is
        accurate and to handle window resizing.
        :param time_delta: time passed in seconds between one call to this method and the next.
        """
        super().update(time_delta)
        
        rect = self.relative_rect
        
        surface = pygame.surface.Surface(rect.size,
                                    flags=pygame.SRCALPHA,
                                    depth=32)
        
        line_size = 2
        gap_size = rect.w / 20
        
        points = [(gap_size, 0), 
                  (0, 0), 
                  (0, rect.height - line_size *2),
                  (gap_size, rect.height - line_size *2)]
        
        pygame.draw.lines(surface, self.decoration_colour, False, points, line_size)
        
        points = [(rect.width - gap_size - line_size * 2, 0), 
                  (rect.width - line_size * 2, 0), 
                  (rect.width - line_size * 2, rect.height - line_size *2), 
                  (rect.width - gap_size - line_size * 2, rect.height - line_size *2)]
        
        pygame.draw.lines(surface, self.decoration_colour, False, points, line_size)
        
        # Temp
        
        dir = os.path.dirname(os.path.abspath(__file__))
        
        big_font = pygame.font.Font(os.path.join(dir, self.font), 36)
        small_font = pygame.font.Font(os.path.join(dir, self.font), 18)
        
        main_label = big_font.render(str(self.value), False, self.decoration_colour)        
        units_label = small_font.render(self.units, False, self.decoration_colour)
        small_label = small_font.render(self.hint, False, self.decoration_colour)
        
        # Value
        top_margin = 10
        left_margin = gap_size * 2
        
        surface.blit(main_label, (left_margin, top_margin))
        
        # Units
        top_margin = top_margin + main_label.get_height()      
          
        surface.blit(units_label, (left_margin + main_label.get_width(), top_margin - units_label.get_height()))
        
        # Progress bar
        progress_value = self.value/(self.max - self.min)
        progress_height = 10
        
        top_margin = top_margin + 5
        
        pygame.draw.rect(surface, self.decoration_colour, (left_margin, top_margin, (rect.width - left_margin * 2) * progress_value, progress_height), 0)
        pygame.draw.line(surface, self.decoration_colour, (left_margin + (rect.width - left_margin * 2), top_margin), (left_margin + (rect.width - left_margin * 2), top_margin + progress_height), 1)
        
        # Hint
        top_margin = top_margin + progress_height + 5
        surface.blit(small_label, (left_margin, top_margin))

        self.set_image(surface)
        
        

