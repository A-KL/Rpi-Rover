import os
import subprocess
import paho.mqtt.client as paho
import config

def on_message(client, userdata, message):
    value = message.payload.decode("utf-8")
    os.system(f"aplay ~/projects/Rover/sound/{value}")

def run():
    mqtt = paho.Client()
    mqtt.connect("127.0.0.1", 1883, 60)
    mqtt.on_message = on_message
    mqtt.subscribe(config.audio_play)

    print("Audio service ready")

    mqtt.loop_forever()

    print("Audio service stopped")

if __name__ == "__main__":
    run()