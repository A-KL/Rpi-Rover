import json

import modules.mqtt_module as mqtt
import config_module as config
import modules.power_module as power_sensor

if __name__ == "__main__":
    client = mqtt.Create()

    voltage, current, power, shunt_voltage = power_sensor.read(0)
    jobject = { "v" : voltage, "i" : current, "p" : power, "sv" :  shunt_voltage}

    client.publish(config.power_logic_topic, json.dumps(jobject))

    voltage, current, power, shunt_voltage = power_sensor.read(1)
    jobject = { "v" : voltage, "i" : current, "p" : power, "sv" :  shunt_voltage}

    client.publish(config.power_main_topic, json.dumps(jobject))