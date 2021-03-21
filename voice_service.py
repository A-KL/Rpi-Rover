import pyttsx3
import mqtt_module as mqtt
import config_module as config

def speak(command):  
    engine.say(command)  
    engine.runAndWait() 

def on_message(client, userdata, message):
    value = message.payload.decode("utf-8")
    speak(value)

if __name__ == "__main__":
    engine = pyttsx3.init() 
    engine.setProperty('volume', 1)
    engine.setProperty('rate', 300)

    # voices = engine.getProperty('voices')
    # for voice in voices:
    #     if voice.name.startswith('english'):
    #         print(f"Name:{voice.name} Id:{voice.id} languages:{voice.languages} Age:{voice.age} Gender:{voice.gender} ")

    engine.setProperty('voice', 'english')

    client = mqtt.Create(config.audio_say, on_message)

    speak("Voice service ready")

    client.loop_forever()