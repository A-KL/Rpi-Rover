from modules.DFRobot_RaspberryPi_Expansion_Board import DFRobot_Expansion_Board_IIC as Board
from modules.DFRobot_RaspberryPi_Expansion_Board import DFRobot_Expansion_Board_Servo as Servo

import modules.mqtt_module as mqtt
import config_module as config

board = Board(1, 0x10)    # Select i2c bus 1, set address to 0x10
servo = Servo(board)

# camera parking
# 3: 70 degree
# 2: 5 degree
# camera work
# 3: 50..125
# 2: 90 degree

def print_board_status():
  if board.last_operate_status == board.STA_OK:
    print("board status: everything ok")

  elif board.last_operate_status == board.STA_ERR:
    print("board status: unexpected error")

  elif board.last_operate_status == board.STA_ERR_DEVICE_NOT_DETECTED:
    print("board status: device not detected")

  elif board.last_operate_status == board.STA_ERR_PARAMETER:
    print("board status: parameter error")

  elif board.last_operate_status == board.STA_ERR_SOFT_VERSION:
    print("board status: unsupport board framware version")

def on_message(client, userdata, message):

    channel = int(message.topic.split("/")[2])
    name = str(message.topic.split("/")[3])
    value = int(message.payload.decode("utf-8"))

    index = int(channel / 16)
    channel = channel % 16

    print(f"Device:{index} Channel:{channel} {name}:{value}")

    # if (name == 'duty_cycle'):
    #     c = devices[index].channels[channel]
    #     # c = pca.channels[channel]
    #     c.duty_cycle = value
    if (name == 'angle'):
      servo.move(channel, value)

if __name__ == "__main__":
    print_board_status()

    board.begin()
    servo.begin()

    client = mqtt.Create(config.pwm_topic, on_message)

    print("GravityIO service ready")

    client.loop_forever()

    print("GravityIO service stopped")    
