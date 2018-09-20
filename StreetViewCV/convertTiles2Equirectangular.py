import math
import numpy as np
import cv2


class convertToEquirect:
	def __init__(self, imgName):
		self.imgName = imgName
		self.front = cv2.imread(self.imgName+'_front.jpg',1)
		self.top = cv2.imread(self.imgName+'_top.jpg',1)
		self.bottom = cv2.imread(self.imgName+'_bottom.jpg',1)
		self.left = cv2.imread(self.imgName+'_left.jpg',1)
		self.right = cv2.imread(self.imgName+'_right.jpg',1)
		self.back = cv2.imread(self.imgName+'_back.jpg',1)
		self.height, self.width, self.channels = self.front.shape
		self.newImage = np.zeros((self.height*2,self.width*2*2,self.channels), np.uint8)
		#print(self.imgName+'_front.jpg')
		#cv2.imshow('image', self.front)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		self.convertCubeMap2Equirect()

	def convertCubeMap2Equirect(self):
		self.convertFace2Equirect(self.front, "front")
		self.convertFace2Equirect(self.top, "right")
		self.convertFace2Equirect(self.bottom, "bottom")
		self.convertFace2Equirect(self.left, "left")
		self.convertFace2Equirect(self.right, "right")
		self.convertFace2Equirect(self.back, "back")
		cv2.imshow('image', self.newImage)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	def convertFace2Equirect(self, face, faceName):
		for i in range(self.width):
			for j in range(self.height):
				cubeWidth = self.width
				newu, newv = self.map_cube(i, j, faceName, cubeWidth, self.width*2, self.height)
				
				self.newImage[int(round(newv)), int(round(newu)), :] = face[j, i, :]

	def get_theta_phi(self, _x, _y, _z):
		dv = math.sqrt(_x*_x + _y*_y + _z*_z)
		x = _x/dv
		y = _y/dv
		z = _z/dv
		theta = math.atan2(y, x)
		phi = math.asin(z)
		return theta, phi


	# x,y position in cubemap
	# cw  cube width
	# W,H size of equirectangular image
	def map_cube(self, x, y, side, cw, W, H):

		u = 2*(float(x)/cw - 0.5)
		v = 2*(float(y)/cw - 0.5)

		if side == "front":
			theta, phi = self.get_theta_phi( 1, u, v )
		elif side == "right":
			theta, phi = self.get_theta_phi( -u, 1, v )
		elif side == "left":
			theta, phi = self.get_theta_phi( u, -1, v )
		elif side == "back":
			theta, phi = self.get_theta_phi( -1, -u, v )
		elif side == "bottom":
			theta, phi = self.get_theta_phi( -v, u, 1 )
		elif side == "top":
			theta, phi = self.get_theta_phi( v, u, -1 )

		_u = 0.5+0.5*(theta/math.pi)
		_v = 0.5+(phi/math.pi)
		return _u*W,  _v*H

convertToEquirect("streetviews/img1")

#print map_cube(194, 175, "right", 250, 1000, 500)