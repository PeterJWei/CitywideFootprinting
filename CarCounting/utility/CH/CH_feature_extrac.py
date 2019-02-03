import os
from scipy.spatial import distance as dist
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import argparse
import glob
import cv2


# Preprocess the images with background subtraction
BLUR = 21
MASK_DILATE_ITER = 10
MASK_ERODE_ITER = 5
MASK_COLOR = (0.0,0.0,0.0)
def preProcess(img):
  gray = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY)
  gray_blur = cv2.GaussianBlur(gray, (15, 15), 0)
  thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 11, 1)
  
  kernel = np.ones((3, 3), np.uint8)
  closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)
  cont_img = closing.copy()
  _, contours, _ = cv2.findContours(cont_img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  contours = sorted(contours, key=cv2.contourArea, reverse=True)
  mask = np.zeros(gray.shape)
  cv2.fillConvexPoly(mask, contours[0], (255))
  mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
  mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
  mask_stack = np.dstack([mask]*3) 
  mask_stack  = mask_stack.astype('float32') / 255.0         
  imgC         = img.copy().astype('float32') / 255.0               

  masked = (mask_stack * imgC[...,:3]) + ((1-mask_stack) * MASK_COLOR) 
  masked = (masked * 255).astype('uint8')     
  tmp = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
  _,alpha = cv2.threshold(tmp,50,255,cv2.THRESH_BINARY)
  b, g, r = cv2.split(masked)

  rgba = [b,g,r, alpha]
  dst = cv2.merge(rgba,4)
  image = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
  hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],[0, 256, 0, 256, 0, 256])
  hist = cv2.normalize(hist,hist).flatten()
  
  return dst,hist,image


def feature_extract_ch(img_array_list):
    feature_list = []
    for img in img_array_list:
        dst,hist,image = preProcess(img)
        feature_list.append(hist)

    return feature_list