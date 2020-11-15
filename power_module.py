from ina219 import INA219, DeviceRangeError

SHUNT_OHMS = 0.1

def read():
    ina = INA219(SHUNT_OHMS, address=0x41)
    ina.configure(ina.RANGE_16V)

    voltage = ina.voltage()

    try:
        current = ina.current()
        power =  ina.power()
        shunt_voltage = ina.shunt_voltage()

        return voltage, current, power, shunt_voltage
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resistor
        print(e)

if __name__ == "__main__":
    voltage, current, power, shunt_voltage = read()

    print("Bus Voltage: %.3f V" % voltage)
    print("Bus Current: %.3f mA" % current)
    print("Power: %.3f mW" % power)
    print("Shunt voltage: %.3f mV" % shunt_voltage)