import adc_driver

acs712_zero_drift_voltage = 595.70
acs712_ref_voltage = 5.0
acs712_max_current = 5000 # mA
acs712_sensitivity = 0.185 #V/A

samples_count = 100

def read(drift = acs712_zero_drift_voltage):
    adc_value = 0
    for i in range(samples_count):
        reading = adc_driver.read(3)
        adc_value += reading[1]

    adc_value = adc_value / samples_count
    raw_voltage = abs(adc_value - acs712_ref_voltage/2)
    current = raw_voltage / acs712_sensitivity
    
    return  current * 1000

if __name__ == "__main__":
    print(read())