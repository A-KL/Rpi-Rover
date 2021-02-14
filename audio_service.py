import os
import subprocess
import mqtt_module as mqtt
import config_module as config

def on_message(client, userdata, message):
    value = message.payload.decode("utf-8")
    os.system(f"aplay -D plughw:CARD=wm8960soundcard,DEV=0 ~/projects/Rover/assets/sound/{value}")

if __name__ == "__main__":
    client = mqtt.Create(config.audio_play, on_message)

    print("Audio service ready")

    client.loop_forever()

    print("Audio service stopped")