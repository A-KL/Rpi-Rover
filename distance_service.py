import board
import busio
import adafruit_tca9548a
from adafruit_bus_device.i2c_device import I2CDevice

# Create I2C bus as normal
i2c = busio.I2C(board.SCL, board.SDA)

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)

if __name__ == "__main__":
    ultrasonic0 = I2CDevice(tca[3], 0x57)

    result = bytearray(3)
    while True:
        ultrasonic0.write(bytes([0x01]))
        ultrasonic0.write_then_readinto(bytes([0x03]), result)
        distance = int.from_bytes(result, "big")
        print(distance)