import i2c_lcd
import network_module as network
import mqtt_module as mqtt
import config_module as config

def on_message(client, userdata, message):
    line = int(message.topic.split("/")[3])
    value = message.payload.decode("utf-8")
    #print(f"Line:{line} Value:{value}")
    lcd.lcd_display_string("                ", line)
    lcd.lcd_display_string(value, line)

if __name__ == "__main__":
    lcd = i2c_lcd.lcd()

    lcd.lcd_clear()

    ip, host = network.get_interface()
    lcd.lcd_display_string(f"IP: {ip}", 1)
    lcd.lcd_display_string(f"{host}", 2)

    client = mqtt.Create(config.lcd_lines, on_message)

    print("LCD service ready")

    client.loop_forever()

    print("LCD service stopped")