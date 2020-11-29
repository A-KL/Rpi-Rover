import json
import mqtt_module as mqtt
import config_module as config
import power_module as power
import ups_module as ups

if __name__ == "__main__":
    ups = ups.UPS()
    client = mqtt.Create()

    voltage = ups.get_voltage()
    capacity = ups.get_capacity()
    
    jobject = { "v" : voltage, "c" : capacity }

    client.publish(config.power_ups_topic, json.dumps(jobject))