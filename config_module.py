motors_topic = "rover/motors/+/+"

motor_0_topic = "rover/motors/0/duty_cycle"
motor_1_topic = "rover/motors/1/duty_cycle"
motor_2_topic = "rover/motors/2/duty_cycle"
motor_3_topic = "rover/motors/3/duty_cycle"
motor_4_topic = "rover/motors/4/duty_cycle"
motor_5_topic = "rover/motors/5/duty_cycle"
motor_14_topic = "rover/motors/14/duty_cycle"
motor_15_topic = "rover/motors/15/duty_cycle"

motor_16_topic = "rover/motors/16/duty_cycle"
motor_17_topic = "rover/motors/17/duty_cycle"
motor_18_topic = "rover/motors/18/duty_cycle"
motor_19_topic = "rover/motors/19/duty_cycle"

servo_0_topic = "rover/motors/0/angle"
servo_1_topic = "rover/motors/1/angle"

lcd_lines = "rover/lcd/lines/+"
lcd_line_1 = "rover/lcd/lines/1"
lcd_line_2 = "rover/lcd/lines/2"

control_camera_topic = "rover/control/camera" 
control_rover_topic = "rover/control/rover" 

power_main_topic = "rover/power/main"
power_logic_topic = "rover/power/logic"
power_ups_topic = "rover/power/ups"

audio_play = "rover/audio/play"
audio_say = "rover/audio/say"

camera_object_detection = "rover/camera/detected"

machine_vision_objects = "rover/machine_vision/objects"

machine_vision_proximity = "rover/machine_vision/proximity"

#################################################

servo_tilt = servo_0_topic
servo_turn = servo_1_topic

motor_1_a = motor_16_topic
motor_1_b = motor_17_topic
motor_2_a = motor_18_topic
motor_2_b = motor_19_topic


# devices = [ 
#     [0x04, "Groove ADC"],
#     [0x19, ""], 
#     [0x27, "16x2 LCD"], 
#     [0x42, "Servo PWM"], 
#     [0x43, "Motor PWM"], 
#     [0x40, "5V Power sensor"], 
#     [0x41, "12V Power sensor"], 
#     [0x70, ""] 
# ]