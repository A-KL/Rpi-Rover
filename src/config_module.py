# PWM Unit#
pwm_topic = "rover/pwm/+/+"

servo_0_topic = "rover/pwm/0/angle"
servo_1_topic = "rover/pwm/1/angle"

# MOTOR Unit #

motors_topic = "rover/motors/+"

encoders_topic_template = "rover/encoders/"
encoders_topic = encoders_topic_template + "+"

encoder_0_topic = "rover/encoders/0"
encoder_1_topic = "rover/encoders/1"
encoder_2_topic = "rover/encoders/2"
encoder_3_topic = "rover/encoders/3"

motor_0_topic = "rover/motors/0"
motor_1_topic = "rover/motors/1"
motor_2_topic = "rover/motors/2"
motor_3_topic = "rover/motors/3"

# LCD #

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

motor_a = motor_0_topic
motor_b = motor_1_topic

# devices = [ 
#     [0x04, "Groove ADC"],
#     [0x19, ""], 
#     [0x27, "16x2 LCD"], 
#     [0x42, "Servo PWM"], 
#     [0x43, "Motor PWM"], 
#     [0x40, "5V Power sensor"], 
#     [0x41, "12V Power sensor"], 
#     [0x56, "DC Motor Unit"], 
#     [0x70, ""] 
# ]