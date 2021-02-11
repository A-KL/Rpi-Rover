import time
import board
import busio

import adafruit_pca9685
from adafruit_motor import servo

import mqtt_module as mqtt
import config_module as config

# class I2CDeviceFactory(object):
#     def __init__(self, baseAddress, factoryMethod, i2c=None):
#         self._baseAddress = baseAddress
#         self._factoryMethod = factoryMethod
#         self._i2c = i2c

#     def get(self, index=0):
#         return self._factoryMethod(self._baseAddress + index, self._i2c)

i2c = busio.I2C(board.SCL, board.SDA)

# factory = I2CDeviceFactory(0x40, adafruit_pca9685.PCA9685)

# pca = adafruit_pca9685.PCA9685(i2c)
# pca.frequency = 50

def create_pca(i2c, address):
    pca = adafruit_pca9685.PCA9685(i2c, address = address)
    pca.frequency = 50
    return pca

devices = [create_pca(i2c, 0x40), create_pca(i2c, 0x43)]

def on_message(client, userdata, message):
    channel = int(message.topic.split("/")[2])
    name = str(message.topic.split("/")[3])
    value = int(message.payload.decode("utf-8"))
    index = int(channel / 16)
    channel = channel % 16

    print(f"Device:{index} Channel:{channel} {name}:{value}")

    if (name == 'duty_cycle'):
        c = devices[index].channels[channel]
        # c = pca.channels[channel]
        c.duty_cycle = value
    elif (name == 'angle'):
        s = servo.Servo(devices[index].channels[channel], min_pulse=600, max_pulse=2600)
        s.angle = value

if __name__ == "__main__":
    client = mqtt.Create(config.motors_topic, on_message)

    print("Motors service ready")

    client.loop_forever()

    print("Motors service stopped")    
