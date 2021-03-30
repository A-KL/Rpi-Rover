import time
import board
import busio

import config_module as config

import modules.mqtt_module as mqtt
import modules.motor_control_module as dc_module

def on_message(client, userdata, message):
    channel = int(message.topic.split("/")[2])
    value = int(message.payload.decode("utf-8"))

    print(f"Channel:{channel} {value}")

    driver.writeSpeed(channel, value)

def push_encoder_message(index):
    value = driver.readEncoder(index)
    client.publish(encoders_topic_template + str(index), value)

if __name__ == "__main__":
    driver = dc_module.DcMotorDriver()
    version = driver.readVersion()

    client = mqtt.Create(config.motors_topic, on_message)

    print("Motors service ready")

    client.loop_start()
    # client.loop_forever()

    while True:
        for i in range(4):
            push_encoder_message(i)
        time.sleep(0.1)

    client.loop_stop(force=False)

    print("Motors service stopped")    
