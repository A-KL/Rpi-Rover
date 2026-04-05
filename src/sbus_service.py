from modules.DFRobot_RaspberryPi_Expansion_Board import *
from modules.read_sbus_from_GPIO import *

import time

if __name__ == "__main__":
    # board = DFRobot_Expansion_Board_IIC(1, 0x10)
    # board.begin()

    # servo = DFRobot_Expansion_Board_Servo(board)
    # servo.begin()

    SBUS_PIN = 4 #pin where sbus wire is plugged in

    reader = SbusReader(SBUS_PIN)
    reader.begin_listen()

    time.sleep(.1)

    while True:
        try:
            is_connected = reader.is_connected()
            packet_age = reader.get_latest_packet_age() #milliseconds

            #returns list of length 16, so -1 from channel num to get index
            channel_data = reader.translate_latest_packet()
            
            #
            #Do something with data here!
            #ex:print(f'{channel_data[0]}')
            #

        except KeyboardInterrupt:
            #cleanup cleanly after ctrl-c
            reader.end_listen()
            exit()
        except:
            #cleanup cleanly after error
            reader.end_listen()
            raise
    
    # servo.move(channel, value)
    
    # client = mqtt.Create(config.pwm_topic, on_message)

    # print("PWM HAT service ready")

    # client.loop_forever()

    # print("PWM HAT service stopped")    
