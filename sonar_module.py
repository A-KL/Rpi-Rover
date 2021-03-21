import time
import struct
import board
import busio
import smbus
import adafruit_tca9548a
from adafruit_bus_device.i2c_device import I2CDevice

class Ultrasonic(object):
    def __init__(self, port=1):
        self.bus = smbus.SMBus(port)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
        self.address = 0x57

    def get_distance(self):
        self.bus.write_byte(self.address, 0x01)
        time.sleep(0.120)
        block = self.bus.read_i2c_block_data(self.address, 3)[0:3]
        distance = block[0] << 16 | block[1] << 8 | block[2]
        return float(distance) / 1000

class UltrasonicI2c(object):
    def __init__(self, i2c, address = 0x57):
        self.bus = i2c
        self.address = address
        self.block = bytearray(3)

    def get_distance(self):
        while not self.bus.try_lock():
            pass

        self.bus.writeto(self.address, bytes([0x01]))
        time.sleep(0.120)
        self.bus.writeto(self.address, bytes([0x03]))
        self.bus.readfrom_into(self.address, self.block)

        self.bus.unlock()

        distance = self.block[0] << 16 | self.block[1] << 8 | self.block[2]
        return float(distance) / 1000

if __name__ == "__main__":
    # Create I2C bus as normal
    i2c = busio.I2C(board.SCL, board.SDA)

    # Create the TCA9548A object and give it the I2C bus
    tca = adafruit_tca9548a.TCA9548A(i2c)

    device0 = UltrasonicI2c(tca[2])    
    device1 = UltrasonicI2c(tca[3])

    while True:
        print(str(device0.get_distance()) + " mm")
        print(str(device1.get_distance()) + " mm")
        time.sleep(1)
        