import paho.mqtt.client

def Create(topic = None, callback = None):
    mqtt = paho.mqtt.client.Client()
    mqtt.connect("127.0.0.1", 1883, 60)

    if (topic and callback):
        mqtt.on_message = callback
        mqtt.subscribe(topic)

    return mqtt