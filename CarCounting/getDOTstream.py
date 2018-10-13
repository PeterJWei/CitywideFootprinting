import urllib2
import cv2
import numpy as np
import web
import base64
from TF_SSD import CarDetector

urls = ("/", "stream",
		"/test", "testCamera")

C = CarDetector('CarCounting/InferenceGraph/frozen_inference_graph.pb')

class stream:
	def GET(self):
		self.G = getStream('http://207.251.86.238/cctv303.jpg?math=0.29673863811952195')
		print("Getting stream...")
		return self.G.getImage()

class testCamera:
	def GET(self):
		im = cv2.imread("CarCounting/pic0.jpg")
		#im = im[:, :, ::-1]
		
		sensitivity = 0.5
		C = CarDetector('CarCounting/InferenceGraph/frozen_inference_graph.pb')
		boxes, scores, classes, num = C.getClassification(im)
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

		retval, b = cv2.imencode('.jpg', im)
		encoded_string = base64.b64encode(b)
		return encoded_string


class getStream:
	def __init__(self, url):
		self.stream = urllib2.urlopen(url)

	def getImage(self):
		file = self.stream.read()
		encoded_string = base64.b64encode(file)
		arr = np.asarray(bytearray(file), dtype=np.uint8)
		img = cv2.imdecode(arr, -1)

		boxes, scores, classes, num = C.getClassification(img)
		limit = 0

		for i in range(scores[0].shape[0]):
			if scores[0][i] < 0.5:
				limit = i
				break
		nBoxes = boxes[0][0:limit]
		nScores = scores[0][0:limit]
		nClasses = classes[0][0:limit]
		#print(nBoxes)

		#Box colors
		R = 0
		G = 255
		B = 0
		for box1 in nBoxes:
			x1 = min(351,int(round(box1[1]*352)))
			y1 = min(239,int(round(box1[0]*240)))
			x2 = min(351,int(round(box1[3]*352)))
			y2 = min(239,int(round(box1[2]*240)))
			img[y1:y2, x1, 0] = R
			img[y1:y2, x1, 1] = G
			img[y1:y2, x1, 2] = B
			img[y1:y2, x2, 0] = R
			img[y1:y2, x2, 1] = G
			img[y1:y2, x2, 2] = B
			img[y1, x1:x2, 0] = R
			img[y1, x1:x2, 1] = G
			img[y1, x1:x2, 2] = B
			img[y2, x1:x2, 0] = R
			img[y2, x1:x2, 1] = G
			img[y2, x1:x2, 2] = B
		#Do some opencv here

		#At the end, convert back to numpy array to present on the localhost

		#arr.tobytes()
		retval, b = cv2.imencode('.jpg', img)
		encoded_string = base64.b64encode(b)
		#encoded_string = base64.b64encode(arr)
		return encoded_string


DOTstream = web.application(urls, locals());