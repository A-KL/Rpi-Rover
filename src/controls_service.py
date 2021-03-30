import json
import modules.mqtt_module as mqtt
import config_module as config

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

    client.publish(config.servo_tilt, tilt)
    client.publish(config.servo_turn, turn)

def updateMotors(x, y):
    motor_0_channel_a, motor_0_channel_b = wheel(y - x)
    motor_1_channel_a, motor_1_channel_b = wheel(y + x)

    client.publish(config.motor_1_a, int(motor_0_channel_a))
    client.publish(config.motor_1_b, int(motor_0_channel_b))
    client.publish(config.motor_2_a, int(motor_1_channel_a))
    client.publish(config.motor_2_b, int(motor_1_channel_b))

def on_message(client, userdata, message):
    global current_servos_y
    global current_servos_x

    global current_motors_y
    global current_motors_x

    service = str(message.topic.split("/")[2])
    payload = json.loads(message.payload.decode("utf-8"))
    x = float(payload["x"])
    y = float(payload["y"])
    
    if (service == "camera"):
        if (y != current_servos_y or x != current_servos_x):
            current_servos_x = x
            current_servos_y = y
            updateServos(current_servos_x, current_servos_y)

    elif (service == "rover"):
        if (y != current_motors_y or x != current_motors_x):
            current_motors_x = x
            current_motors_y = y
            updateMotors(current_motors_x, current_motors_y)

if __name__ == '__main__':
    client = mqtt.Create()

    client.on_message = on_message
    client.subscribe(config.control_camera_topic)
    client.subscribe(config.control_rover_topic)

    print("Ready to receive commands")

    client.loop_forever()
