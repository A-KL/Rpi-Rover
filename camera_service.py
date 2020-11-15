import os
import json
import threading
import time
import socket
import picamera
import network_module as network

class WriteCallbackStream(object):
    def __init__(self, write_callback):
        self.write_callback = write_callback

    def write(self, buf):
        return self.write_callback(buf)

# TODO: Don't use global variable
s = network.cameraConnection()

def on_new_raw_frame(buffer):
    s.sendto(buffer, ("0.0.0.0", 5005))

if __name__ == '__main__':
    stream = WriteCallbackStream(on_new_raw_frame)

    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 12
        camera.start_recording(stream, format='h264', quality=20, profile='baseline')

        # TODO: Find a better way
        while True:
            time.sleep(1)


