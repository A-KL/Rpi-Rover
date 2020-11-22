import os
import json
import threading
import time
import socket
import struct
import sys
import picamera
import network_module as network

camera_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
camera_socket.setblocking(0)

class WriteCallbackStream(object):
    def __init__(self, write_callback):
        self.write_callback = write_callback

    def write(self, buf):
        return self.write_callback(buf)


def on_new_raw_frame(buffer):
    print("Frame sent")
    camera_socket.send(buffer)
    print("Frame sent")

if __name__ == '__main__':
    stream = WriteCallbackStream(on_new_raw_frame)

    if os.path.exists(network.CAMERA_H264_RAW_STREAM):
        os.remove(network.CAMERA_H264_RAW_STREAM)

    camera_socket.bind(network.CAMERA_H264_RAW_STREAM)

    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 12
        camera.start_recording(stream, format='h264', quality=20, profile='baseline')
        print("Streaming has started")

        # TODO: Find a better way
        while True:
            time.sleep(1)

        camera_socket.close()
        os.remove(network.CAMERA_H264_RAW_STREAM)


