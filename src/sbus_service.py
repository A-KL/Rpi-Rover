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
            if not is_connected:
                print("SBUS DISCONNECTED")
                time.sleep(.5)
                continue

            packet_age = reader.get_latest_packet_age() #milliseconds

            #returns list of length 16, so -1 from channel num to get index
            channel_data = reader.translate_latest_packet()
            
            print(f'{channel_data[0]}\t{channel_data[1]}\t{channel_data[2]}\t{channel_data[3]}\t{channel_data[4]}\t{channel_data[5]}\t{channel_data[6]}\t{channel_data[7]}\t{channel_data[8]}\t{channel_data[9]}\t{channel_data[10]}\t{channel_data[11]}\t{channel_data[12]}\t{channel_data[13]}\t{channel_data[14]}\t{channel_data[15]}')
            
        except KeyboardInterrupt:
            #cleanup cleanly after ctrl-c
            reader.end_listen()
            exit()
        except:
            #cleanup cleanly after error
            reader.end_listen()
            raise
    
    reader.end_listen()

    # servo.move(channel, value)
    
    # client = mqtt.Create(config.pwm_topic, on_message)

    # print("PWM HAT service ready")

    # client.loop_forever()

    # print("PWM HAT service stopped")    
