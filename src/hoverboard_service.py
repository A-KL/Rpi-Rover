import serial
import sys
import json

import modules.mqtt_module as mqtt
import modules.motor_control_module as dc_module

def encode_message(x, y):
    speed = int(y * 1000)
    steer = int(x * 1000)

    crc = 0xAAAA ^ speed ^ steer

    return [0xAAAA, speed, steer, crc]

# def on_message(client, userdata, message):
#     channel = int(message.topic.split("/")[2])
#     value = int(message.payload.decode("utf-8"))

#     command = encode_message(0.5, 0.4)
#     uart.write(command)

    # print(f"Channel:{channel} {value}")

    # try:
    #     driver.writeSpeed(channel, value)
    # except OSError as error:
    #     print(error)

if __name__ == "__main__":

    uart = serial.Serial(
            port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
            baudrate = 19200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)

    uart.open()

    print("Hoverboard motors service ready")

    for line in sys.stdin:
        message = json.loads(line)
        x = float(message["x"])
        y = float(message["y"])
        # sender = float(message["sender"])
        command = encode_message(x, y)
        uart.write(command)

    # client = mqtt.Create(config.motors_topic, on_message)
    # client.loop_forever()

    print("Hoverboard motors service stopped")    
