import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 100
img1color = cv2.imread('equirectangular1.png')
img2color = cv2.imread('equirectangular2.png')
img1 = cv2.imread('equirectangular1.png',0)          # queryImage
img2 = cv2.imread('equirectangular2.png',0) # trainImage

# Initiate SIFT detector
orb = cv2.ORB_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)



# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptors.
matches = bf.match(des1,des2)

# Sort them in the order of their distance.
matches = sorted(matches, key = lambda x:x.distance)

# Draw first 10 matches.
img3 = cv2.drawMatches(img1color,kp1,img2color,kp2,matches[:100],None)



plt.imshow(img3),plt.show()