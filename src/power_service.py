import json

import modules.mqtt_module as mqtt
import config_module as config
import modules.ina219_module as ina219_sensor
import modules.ina3221_module as ina3221_sensor

def to_json(device, channel):
    voltage = device.getBusVoltage_V(channel)
    shunt_voltage = ina3221.getShuntVoltage_mV(channel)
    # minus is to get the "sense" right.   - means the battery is charging, + that it is discharging
    current = device.getCurrent_mA(channel)
    power = current * voltage
    # loadvoltage1 = busvoltage1 + (shuntvoltage1 / 1000)

    jobject = { "v" : voltage, "i" : current, "p" : power, "sv" :  shunt_voltage}
    return json.dumps(jobject)

if __name__ == "__main__":
    client = mqtt.Create()

    ina3221 = ina3221_sensor.SDL_Pi_INA3221()

    client.publish(config.power_1_topic, to_json(ina3221, 1))
    client.publish(config.power_2_topic, to_json(ina3221, 2))
    client.publish(config.power_3_topic, to_json(ina3221, 3))

    # voltage, current, power, shunt_voltage = ina219_sensor.read(0)
    # jobject = { "v" : voltage, "i" : current, "p" : power, "sv" :  shunt_voltage}

    # client.publish(config.power_logic_topic, json.dumps(jobject))

    # voltage, current, power, shunt_voltage = ina219_sensor.read(1)
    # jobject = { "v" : voltage, "i" : current, "p" : power, "sv" :  shunt_voltage}

    # client.publish(config.power_main_topic, json.dumps(jobject))