from ina219 import INA219, DeviceRangeError

SHUNT_OHMS = 0.1

def create_ina():
    ina0 = INA219(SHUNT_OHMS, address=0x41)
    ina0.configure(ina0.RANGE_16V)

    ina1 = INA219(SHUNT_OHMS, address=0x44)
    ina1.configure(ina1.RANGE_16V)

    return [ina0, ina1]

devices = create_ina()

def read(index):
    ina = devices[index]

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
    voltage, current, power, shunt_voltage = read(0)

    print("Bus Voltage: %.3f V" % voltage)
    print("Bus Current: %.3f mA" % current)
    print("Power: %.3f mW" % power)
    print("Shunt voltage: %.3f mV" % shunt_voltage)