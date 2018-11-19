import random
import numpy as np
from pyemd import emd_samples
from compute_hog import hog_from_path
from scipy.stats import wasserstein_distance
from scipy.ndimage import imread
from histogram import calc_similar_by_path
import os
class correlationClass:
	def __init__(self, previousBoxes, currentBoxes):
		self.previousBoxes = previousBoxes
		self.currentBoxes = currentBoxes
		self.threshold = 0.9
		self.numCorrelations = 0
		return

	def correlateBoxes(self, prevImage, image):
		correlations = []
		correlationIndices = []

		#maxCorrelation = [0] * len(self.currentBoxes)
		for j in range(len(self.previousBoxes)):
			img1coords = self.previousBoxes[j]
			if prevImage is None:
				return ([], range(len(self.currentBoxes)))
			(x1, x2, y1, y2) = img1coords
			img1 = prevImage[y1:y2, x1:x2]
			for i in range(len(self.currentBoxes)):
				img2coords = self.currentBoxes[i]
				(x1, x2, y1, y2) = img2coords
				img2 = image[y1:y2, x1:x2]
				c = self.correlate(img1, img2)
				correlations.append(c)
				correlationIndices.append((j, i))

		correlations, correlationIndices = zip(*sorted(zip(correlations, correlationIndices), reverse=True))
		correlations = list(correlations)
		correlationIndices = list(correlationIndices)

		maxCorrelation = [None] * len(self.currentBoxes)
		counted = [False] * len(self.previousBoxes)
		for i in range(len(correlations)):
			score = correlations[i]
			if score < self.threshold:
				break
			(prev, curr) = correlationIndices[i]
			if counted[prev]:
				continue
			else:
				maxCorrelation[curr] = prev
				counted[prev] = True

		tracked = []
		new = []
		for i in range(len(maxCorrelation)):
			if maxCorrelation[i] is None:
				new.append(i)
			else:
				tracked.append(i)

		return (tracked, new)

	def correlate(self, img1, img2):
		# self.numCorrelations += 1
		# a = imread(img1)
		# b = imread(img2)
		# a_hist = get_histogram(a)
		# b_hist = get_histogram(b)
		# dist = wasserstein_distance(a_hist, b_hist)
		HOG_1 = hog_from_path(img1)
		HOG_2 = hog_from_path(img2)
		emd_score = emd_samples(HOG_1,HOG_2)
		score = calc_similar_by_path(img1, img2)
		return emd_score, str(score*100)+"%"


if __name__ == "__main__":
	cur_path = os.getcwd()
	# print(correlationClass().correlate(cur_path+"/utility/pic1.png",cur_path+"/utility/pic2.png"))
	#pic2:		 0.01156864434068185, 0.001297264347126175
	#pic3:		 0.00751398291582458, 0.001001572697818916
	#pic_red:	 0.02414210992117115, 0.001267426229206782
	#pic5_black: 0.00584855951159818, 0.001375098944280004