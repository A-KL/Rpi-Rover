import modules.mqtt_module as mqtt
import config_module as config

max_value = 255

def wheel(v):
    if (v > 1):
        v = 1

    if (v < -1):
        v = -1

    return max_value * v
    # if (v > 0):
    #     return v * max_value, 0
    # elif (v < 0):
    #     return 0, (-v) * max_value
    # else:
    #     return 0, 0

def updateServos(client, x, y):
    tilt = 90 + int(90 * y)
        # Fix it: 0..130..180
    turn = 90 + int(90 * x)

    client.publish(config.servo_tilt, tilt)
    client.publish(config.servo_turn, turn)

def updateMotors(client, x, y):
    motor_a = wheel(y + x)
    motor_b = wheel(y - x)

    client.publish(config.motor_a, int(motor_a))
    client.publish(config.motor_b, int(motor_b))