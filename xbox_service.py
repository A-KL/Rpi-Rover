import math
import time
import xbox
import paho.mqtt.client as paho
import config

max_value = 65535

current_servos_x = 0
current_servos_y = 0

current_motors_x = 0
current_motors_y = 0

def wheel(v):
    if (v>1):
        v = 1

    if (v<-1):
        v = -1

    if (v > 0):
        return v * max_value, 0
    elif (v < 0):
        return 0, (-v) * max_value
    else:
        return 0, 0

def updateServos(x, y):
    tilt = 90 + int(90 * y)
        # Fix it: 0..130..180
    turn = 90 + int(90 * x)

    mqtt.publish(config.servo_tilt, tilt)
    mqtt.publish(config.servo_turn, turn)

def updateMotors(x, y):
    motor_0_channel_a, motor_0_channel_b = wheel(y - x)
    motor_1_channel_a, motor_1_channel_b = wheel(y + x)

    mqtt.publish(config.motor_1_a, int(motor_0_channel_a))
    mqtt.publish(config.motor_1_b, int(motor_0_channel_b))
    mqtt.publish(config.motor_2_a, int(motor_1_channel_a))
    mqtt.publish(config.motor_2_b, int(motor_1_channel_b))

def awaitXboxJoystick():
    while True:
        try:
            return xbox.Joystick()
        except IOError as e:
            print(e)
            time.sleep(5) # sec


mqtt = paho.Client()
mqtt.connect("127.0.0.1", 1883, 60)

updateMotors(current_motors_x, current_motors_y)
updateServos(current_servos_x, current_servos_y)

print("Awaiting Xbox Controller..")

joy = awaitXboxJoystick()

print("Xbox Controller ready")

try:
    while not joy.Back():
        x0, y0 = joy.leftStick()
        x1, y1 = joy.rightStick()

        if (y1 != current_servos_y or x1 != current_servos_x):
            current_servos_x = x1
            current_servos_y = y1
            updateServos(current_servos_x, current_servos_y)

        if (y0 != current_motors_y or x0 != current_motors_x):
            current_motors_x = x0
            current_motors_y = y0
            updateMotors(current_motors_x, current_motors_y)

        time.sleep(0.1)
except:
    joy.close()
    mqtt.disconnect()
    print("Xbox Controller disconnected")