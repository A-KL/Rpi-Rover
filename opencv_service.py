import cv2
import time

import paho.mqtt.client as paho
import json

from opencv_driver import *
import config

if __name__ == '__main__':
    mqtt = paho.Client()
    mqtt.connect("127.0.0.1", 1883, 60)

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    print("Video initialized. Loading DNN Detection Model...")

    driver = OpenCVDriver("dnn")
    driver.load()

    print("Model OK!")

    try:
        while True:
            start_time = time.time()
            success, img = cap.read()

            print(f"Frame {time.time() - start_time}sec")

            start_time = time.time()

            result, objectInfo = driver.getObjects(img, 0.45, 0.2, objects=['person','mouse'])

            print(f"Detection {time.time() - start_time}sec")

            if (len(objectInfo) > 0):
                print(objectInfo)
                # mqtt.publish(config.camera_object_detection, objectInfo)
    except:
        cap.release()
        mqtt.disconnect()
        raise