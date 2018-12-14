import random
import numpy as np
#from pyemd import emd_samples
from compute_hog import hog_from_path
from scipy.stats import wasserstein_distance
from scipy.ndimage import imread
from histogram import calc_similar_by_path
from VGG.VGG_feature_extract import feature_extract
from scipy.spatial.distance import correlation
import os

class correlationClass:
	def __init__(self, previousBoxes, currentBoxes):
		self.previousBoxes = previousBoxes
		self.currentBoxes = currentBoxes
		self.threshold = 0.7
		self.numCorrelations = 0
		return

	def correlateBoxes(self, prevImage, image):
		if len(self.previousBoxes) == 0 or len(self.currentBoxes) == 0:
			return ([], range(len(self.currentBoxes)))
		correlations = []
		correlationIndices = []

		previousImgBoxes = []
		currentImgBoxes = []

		for i in range(len(self.previousBoxes)):
			img1coords = self.previousBoxes[i]
			(x1, x2, y1, y2) = img1coords
			img1 = prevImage[y1:y2, x1:x2, :]
			previousImgBoxes.append(img1)

		for i in range(len(self.currentBoxes)):
			img2coords = self.currentBoxes[i]
			(x1, x2, y1, y2) = img2coords
			img2 = image[y1:y2, x1:x2, :]
			currentImgBoxes.append(img2)

		previousBoxesFeature = feature_extract(previousImgBoxes)
		currentBoxesFeature = feature_extract(currentImgBoxes)


		for j in range(len(previousBoxesFeature)):
			# img1coords = self.previousBoxes[j]
			if prevImage is None:
				return ([], range(len(self.currentBoxes)))
			# (x1, x2, y1, y2) = img1coords
			# img1 = prevImage[y1:y2, x1:x2, :]
			for i in range(len(currentBoxesFeature)):
				# img2coords = self.currentBoxes[i]
				# (x1, x2, y1, y2) = img2coords
				# img2 = image[y1:y2, x1:x2, :]

				c = self.correlate(previousBoxesFeature[i], currentBoxesFeature[j])
				correlations.append(c)
				correlationIndices.append((j, i))
		#Double for loop to correlate each pair of bounding boxes O(n*m)

		correlations, correlationIndices = zip(*sorted(zip(correlations, correlationIndices), reverse=True))
		correlations = list(correlations)
		correlationIndices = list(correlationIndices)
		#sort the scores, along with the box indices O(n*m*log(n*m))

		maxCorrelation = [None] * len(self.currentBoxes)
		counted = [False] * len(self.previousBoxes)
		for i in range(len(correlations)): #worst case: O(n*m)
			score = correlations[i]
			if score < self.threshold: #keep looking at scores until we reach the confidence threshold
				break
			(prev, curr) = correlationIndices[i]
			if counted[prev]: #if the bounding box in the previous frame (prev) was already matched
				continue #then prev was already matched with a higher score
			else:
				maxCorrelation[curr] = prev
				counted[prev] = True
		tracked = []
		new = []
		for i in range(len(maxCorrelation)): #worst case O(n*m)
			if maxCorrelation[i] is None:
				new.append(i)
			else:
				tracked.append(i)
		return (tracked, new)

	def correlate(self, preFeature, curFeature):
		#return a correlation score between img1 and img2. The higher the better!

		#Feature for VGG
		return 1-correlation(preFeature,curFeature)

		#self.numCorrelations += 1

		# a = imread(img1)
		# b = imread(img2)
		# a_hist = get_histogram(a)
		# b_hist = get_histogram(b)
		# dist = wasserstein_distance(a_hist, b_hist)
		#HOG_1 = hog_from_path(img1)
		#HOG_2 = hog_from_path(img2)
		#emd_score = emd_samples(HOG_1,HOG_2)
		#score = calc_similar_by_path(img1, img2)
		#return random.uniform(0, 1)#emd_score, str(score*100)+"%"


if __name__ == "__main__":
	cur_path = os.getcwd()
	# print(correlationClass().correlate(cur_path+"/utility/pic1.png",cur_path+"/utility/pic2.png"))
	#pic2:		 0.01156864434068185, 0.001297264347126175
	#pic3:		 0.00751398291582458, 0.001001572697818916
	#pic_red:	 0.02414210992117115, 0.001267426229206782
	#pic5_black: 0.00584855951159818, 0.001375098944280004