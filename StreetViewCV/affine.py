import cv2
import numpy as np
from matplotlib import pyplot as plt
img = cv2.imread('streetviews/test/testImages_1.jpg')
rows,cols,ch = img.shape

pts1 = np.float32([[0,227], [639,0],[0,400],[639,591]])
pts2 = np.float32([[0,0],[639,0], [0,639],[639,639]])

M = cv2.getPerspectiveTransform(pts1, pts2)
dat = cv2.warpPerspective(img, M, (639, 639))

plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(dat),plt.title('Output')
plt.show()