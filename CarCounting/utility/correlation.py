import random
class correlationClass:
	def __init__(self, previousBoxes, currentBoxes):
		self.previousBoxes = previousBoxes
		self.currentBoxes = currentBoxes
		self.threshold = 0.9
		self.numCorrelations = 0
		return

	def correlateBoxes(self, image):
		maxCorrelation = [0] * len(self.currentBoxes)
		for img1coords in self.previousBoxes:
			(x1, x2, y1, y2) = img1coords
			img1 = image[y1:y2, x1:x2]
			for i in range(len(self.currentBoxes)):
				img2coords = self.currentBoxes[i]
				(x1, x2, y1, y2) = img2coords
				img2 = image[y1:y2, x1:x2]
				c = self.correlate(img1, img2)
				if c > maxCorrelation[i]:
					maxCorrelation[i] = c
		tracked = []
		new = []
		for i in range(len(maxCorrelation)):
			if maxCorrelation[i] > self.threshold:
				tracked.append(i)
			else:
				new.append(i)
		return (tracked, new)
		

	def correlate(self, img1, img2):
		self.numCorrelations += 1
		return random.uniform(0, 1)