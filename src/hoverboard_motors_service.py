import time
import serial
import board
import busio
import itertools
from itertools import chain
import config_module as config

import modules.mqtt_module as mqtt
import modules.motor_control_module as dc_module

def encode_message(x, y):
    speed = int(y * 1000)
    steer = int(x * 1000)

    crc = 0xAAAA ^ speed ^ steer

    return [0xAAAA, speed, steer, crc]

def on_message(client, userdata, message):
    channel = int(message.topic.split("/")[2])
    value = int(message.payload.decode("utf-8"))

    command = encode_message(0.5, 0.4)
    uart.write(command)

    # print(f"Channel:{channel} {value}")

    # try:
    #     driver.writeSpeed(channel, value)
    # except OSError as error:
    #     print(error)

if __name__ == "__main__":
    command = encode_message(0.5, 0.4)
    command = map(lambda x: x.to_bytes(2, 'little'), command)
    command = chain.from_iterable(command)
    command = list(command)

    print (command)
    exit()

    uart = serial.Serial(
            port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
            baudrate = 19200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)

    client = mqtt.Create(config.motors_topic, on_message)

    print("Hoverboard motors service ready")

    client.loop_forever()

    print("Hoverboard motors service stopped")    
