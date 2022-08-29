from __future__ import print_function
#from inputs import get_gamepad
import inputs

if __name__ == "__main__":
    # gamepad=None
    
    # if not gamepad:
    #     gamepad = inputs.devices.gamepads[0]

    while 1:
        events = inputs.get_gamepad()
        for event in events:
            print(event.ev_type, event.code, event.state)

            if event.code == 'ABS_X': # Left stick X
                print(event.state)

            if event.code == 'ABS_RZ': # Right stick
                print(event.state)

            if event.code == 'ABS_Z': # Left stick
                print(event.state)
