import json
import time
import steering_service as steering
import modules.mqtt_module as mqtt
import config_module as config

classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']
    
def on_person(x, y, w, h):
    print("Person found ")

    motor_x = 0
    motor_y = 0

    screen_mid = 320 / 2
    mid = (x + w / 2) - screen_mid
    motor_x = mid / screen_mid # 1..0..-1

    if h == 240: # max
        if w == 320:            
            motor_y = -0.5 # go back, too close
    else:
        motor_y = 0.5 # go closer, too far

    print("X value: " + str(motor_x))
    print("Y value: " + str(motor_y))

    steering.updateMotors(client, motor_x, motor_y)
    # time.sleep(200)
    # steering.updateMotors(client, 0, 0)
    

def on_message(client, userdata, message):
    raw = message.payload.decode("utf-8")
    print(raw)

    if message.topic == config.machine_vision_objects:
        objects = json.loads(raw)
        for obj in objects:
            index = obj['classid']
            if index == 14:
                x = obj['x']
                y = obj['y']
                w = obj['w']
                h = obj['h']
                on_person(x, y, w, h)

    elif message.topic == "rover/ai-service/enabled":
        client.publish(config.servo_3_topic, 70)
        time.sleep(1)
        if raw == "0":
            client.publish(config.servo_2_topic, 5)
            
        elif raw == "1":
            client.publish(config.servo_2_topic, 90)
            time.sleep(1)
            client.publish(config.servo_3_topic, 90)

if __name__ == "__main__":    
    client = mqtt.Create()
    client.on_message = on_message
    client.subscribe([("rover/ai-service/enabled",0),(config.machine_vision_objects,0)])
    client.loop_forever()