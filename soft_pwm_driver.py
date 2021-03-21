import RPi.GPIO as GPIO
from time import sleep

if __name__ == "__main__":
    GPIO.setwarnings(False)			#disable warnings
    GPIO.setmode(GPIO.BCM)		#set pin numbering system

    GPIO.setup(12, GPIO.OUT)

    pi_pwm = GPIO.PWM(12, 50)	#create PWM instance with frequency
    pi_pwm.start(1)

    while 1:
        value = input('Press return to stop (1..7..12):')   # use raw_input for Python 2
        pi_pwm.ChangeDutyCycle(float(value))

    pi_pwm.stop()

    GPIO.cleanup()