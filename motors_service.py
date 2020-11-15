import time
import board
import busio

import adafruit_pca9685
from adafruit_motor import servo

import mqtt_module as mqtt
import config_module as config

i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)
pca.frequency = 50

def on_message(client, userdata, message):
    channel = int(message.topic.split("/")[2])
    name = str(message.topic.split("/")[3])
    value = int(message.payload.decode("utf-8"))

    print(f"Channel:{channel} Name:{name} Value:{value}")

    if (name == 'duty_cycle'):
        c = pca.channels[channel]
        c.duty_cycle = value
    elif (name == 'angle'):
        s = servo.Servo(pca.channels[channel], min_pulse=600, max_pulse=2600)
        s.angle = value

if __name__ == "__main__":    
    client = mqtt.Create()
    client.on_message = on_message
    client.subscribe(config.motors_topic)

    print("Motors service ready")

    client.loop_forever()

    print("Motors service stopped")    
    pca.deinit()
