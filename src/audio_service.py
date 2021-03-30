import os
import subprocess
import pyttsx3
import mqtt_module as mqtt
import config_module as config

def on_message(client, userdata, message):
    value = message.payload.decode("utf-8")

    if message.topic == config.audio_play:
        os.system(f"aplay ~/projects/Rover/assets/sound/{value}")

    elif message.topic == config.audio_say:
        engine.say(value)  
        engine.runAndWait()

if __name__ == "__main__":
    engine = pyttsx3.init() 

    engine.setProperty('volume', 1)
    engine.setProperty('rate', 150)
    engine.setProperty('voice', 'english')

    client = mqtt.Create()
    client.on_message = on_message
    client.subscribe([(config.audio_play, 0), (config.audio_say, 0)])

    print("Audio service ready")

    client.loop_forever()

    print("Audio service stopped")