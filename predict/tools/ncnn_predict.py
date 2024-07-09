'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-05-06 11:33:32
LastEditors: wds-dxh wdsnpshy@163.com
LastEditTime: 2024-07-07 17:35:58
FilePath: \predict\tools\ncnn_predict.py
Description: 
微信: 15310638214 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-dxh}, All Rights Reserved. 
'''
import time
import os
os.environ['YOLO_VERBOSE'] = str(False)#不打印yolov8信息
from ultralytics import YOLO        # pip install ultralytics -i https://pypi.tuna.tsinghua.edu.cn/simple
import cv2



class yolov8_wds:
    def __init__(self,  model_path=r'D:\OneDrive\workspace\now\Raspberry_helmet_detection\predict\models\best.pt'):
        self.model = YOLO(model_path)


    def convert_boxes(self, boxes):
        xywh = boxes.xywh
        xywh = xywh.tolist()
        #将二维列表转化为整数二维列表
        xywh = [[int(j) for j in i] for i in xywh]
        cls = boxes.cls
        cls = cls.tolist()
        cls = [int(i) for i in cls]
        return xywh,cls
    
    def process_frame(self, frame):
        results = self.model(frame)
        annotated_frame = results[0].plot()
        boxes = results[0].boxes
        xywh, cls = self.convert_boxes(boxes)
        return annotated_frame, xywh, cls
    
    def __del__(self):
        del self.model


if __name__ == '__main__':

    yolo = yolov8_wds()
    cap = cv2.VideoCapture(r"test.mp4")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame, xywh, cls = yolo.process_frame(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break