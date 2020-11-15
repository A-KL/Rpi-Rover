import os
import subprocess
import mqtt_module as mqtt
import config_module as config

def on_message(client, userdata, message):
    value = message.payload.decode("utf-8")
    os.system(f"aplay ~/projects/Rover/artifatcs/sound/{value}")

if __name__ == "__main__":
    client = mqtt.Create()
    client.on_message = on_message
    client.subscribe(config.audio_play)

    print("Audio service ready")

    client.loop_forever()

    print("Audio service stopped")