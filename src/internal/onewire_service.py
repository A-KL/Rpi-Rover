import board
import adafruit_ds18x20
from adafruit_onewire.bus import OneWireBus

ow_bus = OneWireBus(board.D5)

devices = ow_bus.scan()

for device in devices:
    print("ROM = {} \tFamily = 0x{:02x}".format([hex(i) for i in device.rom], device.family_code))


ds18b20 = adafruit_ds18x20.DS18X20(ow_bus, devices[0])
print('Temperature: {0:0.3f} °C'.format(ds18b20.temperature))