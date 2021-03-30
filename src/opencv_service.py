import cv2
import time
import json
import config_module as config
import mqtt_module as mqtt
import opencv_module as opencv

if __name__ == '__main__':
    client = mqtt.Create()

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    print("Video initialized. Loading DNN Detection Model...")

    driver = opencv.OpenCVDriver("artifatcs/dnn")
    driver.load()

    print("Model OK!")

    try:
        while True:
            start_time = time.time()
            success, img = cap.read()

            print(f"Frame {time.time() - start_time}sec")

            start_time = time.time()

            result, objectInfo = driver.getObjects(img, 0.45, 0.2) 
            # , objects=['person','mouse']

            print(f"Detection {time.time() - start_time}sec")

            if (len(objectInfo) > 0):
                print(objectInfo)
                # client.publish(config.camera_object_detection, objectInfo)
    except:
        cap.release()
        client.disconnect()
        raise