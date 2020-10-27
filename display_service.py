import i2c_lcd
import paho.mqtt.client as paho
import network_utils
import config

lcd = i2c_lcd.lcd()

def on_message(client, userdata, message):
    line = int(message.topic.split("/")[3])
    value = message.payload.decode("utf-8")
    #print(f"Line:{line} Value:{value}")
    lcd.lcd_display_string("                ", line)
    lcd.lcd_display_string(value, line)

def run():
    lcd.lcd_clear()

    ip, host = network_utils.get_interface()
    lcd.lcd_display_string(f"IP: {ip}", 1)
    lcd.lcd_display_string(f"{host}", 2)

    mqtt = paho.Client()
    mqtt.connect("127.0.0.1", 1883, 60)
    mqtt.on_message = on_message
    mqtt.subscribe(config.lcd_lines)

    print("LCD service ready")

    mqtt.loop_forever()

    print("LCD service stopped")

if __name__ == "__main__":
    run()