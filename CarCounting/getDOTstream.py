import urllib2
import cv2
import numpy as np
import web
import base64

urls = ("/", "stream")

class stream:
	def __init__(self):
		print("stream")

	def GET(self):
		self.G = getStream('http://207.251.86.238/cctv303.jpg?math=0.29673863811952195')
		print("Getting stream...")
		return self.G.getImage()

class getStream:
	def __init__(self, url):
		self.stream = urllib2.urlopen(url)

	def getImage(self):
		file = self.stream.read()
		encoded_string = base64.b64encode(file)
		arr = np.asarray(bytearray(file), dtype=np.uint8)
		img = cv2.imdecode(arr, -1)
		#byteString = file.decode("utf-8")
		#cv2.imshow('image', img)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		return encoded_string


DOTstream = web.application(urls, locals());