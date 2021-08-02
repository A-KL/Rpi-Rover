import os
import subprocess
import pyttsx3
import modules.mqtt_module as mqtt
import config_module as config

def on_message(client, userdata, message):
    play(message.topic, message.payload.decode("utf-8"))

def play(destination, data):
    if destination == config.audio_play:
        os.system(f"aplay ~/projects/Rover/assets/sound/{data}")

    # curl -L --retry 30 --get --fail \
    # --data-urlencode "text=Hello World!" \
    # "https://glados.c-net.org/generate" | aplay

    elif destination == config.audio_say:
        engine.say(data)  
        engine.runAndWait()

    elif destination == "glados":
        os.system(f"curl -L --retry 30 --get --fail --data-urlencode \"text={data}\" \"https://glados.c-net.org/generate\" | aplay")

    print("Audio playback done")

if __name__ == "__main__":
    engine = pyttsx3.init() 

    engine.setProperty('volume', 1)
    engine.setProperty('rate', 150)
    engine.setProperty('voice', 'english')

    client = mqtt.Create()
    client.on_message = on_message
    client.subscribe(config.audio_any)

    play(config.audio_say, "Voice service ready")

    print("Audio service ready")

    client.loop_forever()

    print("Audio service stopped")