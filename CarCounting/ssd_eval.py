import urllib2
#import urllib.request
import cv2
import numpy as np
import web
import base64
from TF_SSD import CarDetector
from utility.correlation import correlationClass
import json
import time
import os

sensitivity = 0.5
C = CarDetector('CarCounting/InferenceGraph/citycam_graph.pb') #frozen_inference_graph.pb

def get_classified_im(name):
    im = cv2.imread("CarCounting/test_videos/images/{}.jpg".format(name))
    t1 = time.time()
    boxes, scores, classes, num = C.getClassification(im)
    t2 = time.time()
    print("time",t2-t1)
    for i in range(scores[0].shape[0]):
        if scores[0][i] < sensitivity:
            limit = i
            break
    nBoxes = boxes[0][0:limit]
    nScores = scores[0][0:limit]
    nClasses = classes[0][0:limit]

    #Box colors
    R = 0
    G = 255
    B = 0
    for box1 in nBoxes:
        x1 = min(351,int(round(box1[1]*352)))
        y1 = min(239,int(round(box1[0]*240)))
        x2 = min(351,int(round(box1[3]*352)))
        y2 = min(239,int(round(box1[2]*240)))
        im[y1:y2, x1, 0] = R
        im[y1:y2, x1, 1] = G
        im[y1:y2, x1, 2] = B
        im[y1:y2, x2, 0] = R
        im[y1:y2, x2, 1] = G
        im[y1:y2, x2, 2] = B
        im[y1, x1:x2, 0] = R
        im[y1, x1:x2, 1] = G
        im[y1, x1:x2, 2] = B
        im[y2, x1:x2, 0] = R
        im[y2, x1:x2, 1] = G
        im[y2, x1:x2, 2] = B

    # cv2.namedWindow("Image")
    # cv2.imshow("Image", im)
    # cv2.waitKey (0)
    cv2.imwrite("CarCounting/test_videos/ssd/{}_1.jpg".format(name), im)


img_list = os.listdir("CarCounting/test_videos/images")

for img in img_list:
    name , _ = img.split(".")
    get_classified_im(name)

