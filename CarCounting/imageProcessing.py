import numpy as np
import cv2

img = cv2.imread('pic123.jpg')
print(img.shape)
mask = np.zeros(img.shape[:2], np.uint8)

for i in range(img.shape[0]):
	for j in range(img.shape[1]):
		condition1 = (i < 144)
		m = -120.0/147
		b = 144.0 - m * 50
		condition2 = (i < m*j + b)
		m = 103.0/71
		b = 128.0 - m * 293
		condition3 = (i < m*j + b)
		condition4 = i < 129
		if not ((condition1 & condition2) | (condition3 & condition4)):# or (condition3 and condition4)):
			mask[i][j] = 255

res = cv2.bitwise_and(img, img, mask=mask)

for i in range(img.shape[0]):
	for j in range(img.shape[1]):
		if i < 50:
			mask[i][j] = 0

mask2 = np.zeros(img.shape[:2], np.uint8)
for i in range(img.shape[0]):
	for j in range(img.shape[1]):
		if i < 50:
			mask2[i][j] = 192
		else:
			mask2[i][j] = 255



res2 = cv2.bitwise_and(img, img, mask=mask)
res2 = cv2.bitwise_or(res2, mask2)
cv2.imwrite('environmentFiltered.jpg', res)
cv2.imwrite('horizon.jpg', res2)