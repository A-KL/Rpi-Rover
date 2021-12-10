import pygame

pygame.init()

# Initialize the joysticks
pygame.joystick.init()

joystick_count = pygame.joystick.get_count()

# For each joystick:
for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()

    # textPrint.Print(screen, "Joystick {}".format(i) )
    # textPrint.indent()

    # Get the name from the OS for the controller/joystick
    name = joystick.get_name()
    # textPrint.Print(screen, "Joystick name: {}".format(name) )
    
    # Usually axis run in pairs, up/down for one, and left/right for
    # the other.
    axes = joystick.get_numaxes()
    # textPrint.Print(screen, "Number of axes: {}".format(axes) )
    # textPrint.indent()
    
    for i in range( axes ):
        axis = joystick.get_axis( i )
    #     textPrint.Print(screen, "Axis {} value: {:>6.3f}".format(i, axis) )
    # textPrint.unindent()
        
    buttons = joystick.get_numbuttons()
    # textPrint.Print(screen, "Number of buttons: {}".format(buttons) )
    # textPrint.indent()

    for i in range( buttons ):
        button = joystick.get_button( i )
    #     textPrint.Print(screen, "Button {:>2} value: {}".format(i,button) )
    # textPrint.unindent()
        
    # Hat switch. All or nothing for direction, not like joysticks.
    # Value comes back in an array.
    hats = joystick.get_numhats()
    # textPrint.Print(screen, "Number of hats: {}".format(hats) )
    # textPrint.indent()

    for i in range( hats ):
        hat = joystick.get_hat( i )
    #     textPrint.Print(screen, "Hat {} value: {}".format(i, str(hat)) )
    # textPrint.unindent()
    
    # textPrint.unindent()
