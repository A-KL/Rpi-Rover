import sys
import math
import time

import config_module as config
import steering_service as steering

import modules.xbox_module as xbox
import modules.mqtt_module as mqtt

current_servos_x = 0
current_servos_y = 0

current_motors_x = 0
current_motors_y = 0

def awaitXboxJoystick():
    while True:
        try:
            return xbox.Joystick()
        except IOError as e:
            print(e)
            time.sleep(5) # sec

if __name__ == '__main__':
    client = mqtt.Create()

    steering.updateMotors(client, current_motors_x, current_motors_y)
    steering.updateServos(client, current_servos_x, current_servos_y)

    print("Awaiting Xbox Controller..")
    
    joy = awaitXboxJoystick()

    print("Xbox Controller ready")

    try:
        while not joy.Back():
            x0, y0 = joy.leftStick()
            y0 = joy.rightTrigger() - joy.leftTrigger()

            x1, y1 = joy.rightStick()

            x1 = - x1
            y1 = - y1

            if (y1 != current_servos_y or x1 != current_servos_x):
                current_servos_x = x1
                current_servos_y = y1
                steering.updateServos(client, current_servos_x, current_servos_y)

            if (y0 != current_motors_y or x0 != current_motors_x):
                current_motors_x = x0
                current_motors_y = y0
                steering.updateMotors(client, current_motors_x, current_motors_y)

            time.sleep(0.1)
    except Exception as error:
        joy.close()
        client.disconnect()
        print(f"Xbox Controller disconnected: {error}")