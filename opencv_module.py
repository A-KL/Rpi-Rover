class OpenCVDriver(object):
    os = __import__('os')
    cv2 = __import__('cv2')
    np = __import__('numpy')
    
    def __init__(self, dir = '/'):
        self.classNames = []
        root = self.os.path.dirname(__file__)
        self.path = self.os.path.join(root, dir)
        self.classFile = self.os.path.join(self.path, 'coco.names') 
        self.configPath = self.os.path.join(self.path, 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt') 
        self.weightsPath = self.os.path.join(self.path, 'frozen_inference_graph.pb') 

    def load(self):
        with open(self.classFile, 'rt') as f:
            self.classNames = f.read().rstrip('\n').split('\n')

        self.net = self.cv2.dnn_DetectionModel(self.weightsPath, self.configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0/ 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

    def getObjects(self, img, thres, nms, draw=True, objects=[]):
        if len(objects) == 0: 
            objects = self.classNames

        classIds, confs, bbox = self.net.detect(img, confThreshold=thres, nmsThreshold=nms)    
        
        if len(objects) == 0: 
            objects = self.classNames

        objectInfo =[]

        if len(classIds) != 0:
            for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
                className = self.classNames[classId-1]

                if className in objects:
                    obj = [box, [int(box[0] + box[2] / 2), int(box[1] + box[3] / 2)] , className]
                    objectInfo.append(obj)

                    if (draw):
                        self.cv2.circle(img, (obj[1][0], obj[1][1]), 5, color=(0,255,0), thickness=2, lineType=self.cv2.FILLED)

                if (draw):
                    self.cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    self.cv2.putText(img,className.upper(),(box[0]+10,box[1]+30), self.cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    self.cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30), self.cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

        return img, objectInfo