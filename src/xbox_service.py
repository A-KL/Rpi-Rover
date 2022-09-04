import time
import json
import os

import config_module as config
import modules.xbox_module as xbox
import modules.mqtt_module as mqtt

def awaitXboxJoystick():
    while True:
        try:
            return xbox.Joystick()
        except IOError as e:
            print(e)
            time.sleep(5) # sec

def send(client, topic, x, y):
    client.publish(topic, json.dumps({ "x" : x, "y": y, "source":os.path.basename(__file__)}))
    client.publish(topic + '/x', x) 
    client.publish(topic + '/y', y) 

if __name__ == '__main__':
    current_servos_x = 0
    current_servos_y = 0
    current_motors_x = 0
    current_motors_y = 0

    client = mqtt.Create()

    print("Awaiting Xbox Controller..")
    
    joy = awaitXboxJoystick()

    print("Xbox Controller ready")

    try:
        while not joy.Back():
            x0, y0 = joy.leftStick()
            y0 = joy.rightTrigger() - joy.leftTrigger()

            x0 = round(x0, 2)
            y0 = round(y0, 2)

            x1, y1 = joy.rightStick()
            x1 = - round(x1, 2)
            y1 = - round(y1, 2)

            if (y0 != current_motors_y or x0 != current_motors_x):
                current_motors_x = x0
                current_motors_y = y0
                send(client, config.steering_0_topic, current_motors_x, current_motors_y)

            if (y1 != current_servos_y or x1 != current_servos_x):
                current_servos_x = x1
                current_servos_y = y1
                send(client, config.steering_1_topic, current_servos_x, current_servos_y)

            time.sleep(0.05)

    except Exception as error:
        joy.close()

        send(client, config.steering_0_topic, 0, 0)
        send(client, config.steering_1_topic, 0, 0)
        
        client.disconnect()
        print(f"Xbox Controller disconnected: {error}")