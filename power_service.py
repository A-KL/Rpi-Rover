import json

import mqtt_module as mqtt
import config_module as config
import power_module as power

if __name__ == "__main__":
    client = mqtt.Create()

    voltage, current, power, shunt_voltage = power.read()
    jobject = { "v" : voltage, "i" : current, "p" : power, "sv" :  shunt_voltage}

    client.publish(config.power_logic_topic, json.dumps(jobject))

    # main_i = acs712.read()

    # jobject = { "v" : 0, "i" : main_i, "p" : 0}

    # client.publish(config.power_main_topic, json.dumps(jobject))