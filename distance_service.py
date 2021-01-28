import time
import json
import struct
import board
import busio
import smbus
import adafruit_tca9548a
from adafruit_bus_device.i2c_device import I2CDevice

import mqtt_module as mqtt
import config_module as config
from sonar_module import *

if __name__ == "__main__":
    client = mqtt.Create()

    # Create I2C bus as normal
    i2c = busio.I2C(board.SCL, board.SDA)

    # Create the TCA9548A object and give it the I2C bus
    tca = adafruit_tca9548a.TCA9548A(i2c)

    device2 = UltrasonicI2c(tca[2])    
    device3 = UltrasonicI2c(tca[3])

    while True:
        jobject = { "left" : device2.get_distance(), "right" : device3.get_distance()}
        client.publish(config.machine_vision_proximity, json.dumps(jobject))
        time.sleep(1)