import cv2
import os
import numpy as np
import urllib.request
import time
 
#img_root = "pics/"
c = 1
start = 1
while True:
    time.sleep(0.9)
    if start:
        f = open(str(c)+".jpg",'wb')
        f.write(urllib.request.urlopen('http://207.251.86.238/cctv797.jpg?math=0.7047167205090428').read())
        f.close()
        start = 0
    else:
        prev = cv2.imread(str(c)+".jpg")
        cur = urllib.request.urlopen('http://207.251.86.238/cctv797.jpg?math=0.7047167205090428').read()
        TF = prev == cur
        print(TF)
        if TF:
            continue
        else:
            f = open(str(c)+".jpg",'wb')
            f.write(cur)
            f.close()
    c += 1













#frame = cv2.imread(img_root+'2.jpg')
#frame_width= len(frame[0])
#frame_height = len(frame)
#
#out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 1, (frame_width,frame_height))
#
#img_num = len(os.listdir(img_root))
#n = 1
## lower the frame rate
#while n < img_num+1:
#    frame = cv2.imread(img_root+str(n)+'.jpg')
#    out.write(frame)
#    n +=5
#
## for img_name in range(1,img_num+1):
##     frame = cv2.imread(img_root+str(img_name)+'.jpg')
##     out.write(frame)
#
#out.release()
