import config
import board
import busio
import adafruit_ads1x15.ads1115 as ADC
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADC.ADS1115(i2c)
ads.gain = 2/3

def resolution():
    return 2 ^ 15

# should be 0, 1, 2, 3 (ADC.P0)
def read(pin):
    result = AnalogIn(ads, pin)
    return [result.value, result.voltage]

def run():
    print(read(ADC.P1))

if __name__ == "__main__":
    run()