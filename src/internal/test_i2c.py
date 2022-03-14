
import smbus
import time
bus = smbus.SMBus(1)
address = 0x56

for x in range(100):
    bus.write_i2c_block_data(address, 0x00, [0x01, 0xFF])
    print(x)

# print(bus.read_byte_data(address, 0x64))
