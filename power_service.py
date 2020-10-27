import paho.mqtt.client as paho
import json
import config
import power_driver
import adc_driver
import acs712

def run():
    mqtt = paho.Client()
    mqtt.connect("127.0.0.1", 1883, 60)

    voltage, current, power, shunt_voltage = power_driver.read()
    jobject = { "v" : voltage, "i" : current, "p" : power, "sv" :  shunt_voltage}

    mqtt.publish(config.power_logic_topic, json.dumps(jobject))

    main_i = acs712.read()

    jobject = { "v" : 0, "i" : main_i, "p" : 0}

    mqtt.publish(config.power_main_topic, json.dumps(jobject))


if __name__ == "__main__":
    run()