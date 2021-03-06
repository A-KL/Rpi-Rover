import smbus
import busio
import board
from adafruit_bus_device.i2c_device import I2CDevice

class DcMotorDriver(object):
    def __init__(self, address=0x56, port=1):
        self.address = address
        self.MOTOR_ADDR_BASE = 0x00
        self.ENCODER_ADDR_BASE = 0x08

        i2c = busio.I2C(board.SCL, board.SDA)
        self.device = I2CDevice(i2c, address)

    def readVersion(self):
        self.device.write(bytes([0x64]))
        result = bytearray(1)
        self.device.readinto(result)
        return "".join("{:02x}".format(x) for x in result)

    def readEncoder(self, index):
        address = self.ENCODER_ADDR_BASE  + index * 4
        self.device.write(bytes([address]))
        result = bytearray(4)
        self.device.readinto(result)
        return "".join("{:02x}".format(x) for x in result)

    def writeSpeed(self, index: int, speed: int):
        address = self.MOTOR_ADDR_BASE  + index * 2
        payload = bytearray([address])
        payload.extend(speed.to_bytes(2, 'big'))
        self.device.write(payload)               

if __name__ == "__main__":
    driver = DcMotorDriver()
    version = driver.readVersion()

    encoder0 = driver.readEncoder(0)
    encoder1 = driver.readEncoder(1)

    motor0 = driver.writeSpeed(0, 500)

    print(version)
    print(encoder0)
    print(encoder1)