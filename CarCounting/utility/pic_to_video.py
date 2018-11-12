import cv2
import os
import numpy as np
 
img_root = "pic_dashcam/"
frame = cv2.imread(img_root+'2.jpg')
frame_width= len(frame[0])
frame_height = len(frame)

out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 1, (frame_width,frame_height))

img_num = len(os.listdir(img_root))
n = 1
# lower the frame rate
while n < img_num+1:
    frame = cv2.imread(img_root+str(n)+'.jpg')
    out.write(frame)
    n +=5

# for img_name in range(1,img_num+1):
#     frame = cv2.imread(img_root+str(img_name)+'.jpg')
#     out.write(frame)

out.release()
