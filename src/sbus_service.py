from modules.DFRobot_RaspberryPi_Expansion_Board import *
from modules.read_sbus_from_GPIO import *

import time

def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

if __name__ == "__main__":
    SBUS_PIN = 16
    SBUS_MIN = 172
    SBUS_MAX = 2000

    board = DFRobot_Expansion_Board_IIC(1, 0x10)
    board.begin()

    servo = DFRobot_Expansion_Board_Servo(board)
    servo.begin()

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
            
            for i in range(4):
                channel_val = channel_data[i]
                # print(f"Channel {i} value: {channel_val}")
                servo.move(i, arduino_map(channel_val, SBUS_MIN, SBUS_MAX, 0, 180))
            
                # print(f'{channel_data[0]}\t{channel_data[1]}\t{channel_data[2]}\t{channel_data[3]}\t{channel_data[4]}\t{channel_data[5]}\t{channel_data[6]}\t{channel_data[7]}\t{channel_data[8]}\t{channel_data[9]}\t{channel_data[10]}\t{channel_data[11]}\t{channel_data[12]}\t{channel_data[13]}\t{channel_data[14]}\t{channel_data[15]}')
            
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
    

