import sys
import math
import time
import json
import os

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
                client.publish(config.steering_1_topic, json.dumps({ "x" : current_servos_x, "y": current_servos_y, "source":os.path.basename(__file__)}))
                client.publish(config.steering_1_x_topic, current_servos_x) 
                client.publish(config.steering_1_y_topic, current_servos_y) 
                steering.updateServos(client, current_servos_x, current_servos_y)

            if (y0 != current_motors_y or x0 != current_motors_x):
                current_motors_x = x0
                current_motors_y = y0
                client.publish(config.steering_0_topic, json.dumps({ "x" : current_motors_x, "y": current_motors_y, "source":os.path.basename(__file__) }))
                client.publish(config.steering_0_x_topic, current_motors_x) 
                client.publish(config.steering_0_y_topic, current_motors_y) 
                steering.updateMotors(client, current_motors_x, current_motors_y)

            time.sleep(0.1)

    except Exception as error:
        joy.close()
        client.disconnect()
        print(f"Xbox Controller disconnected: {error}")