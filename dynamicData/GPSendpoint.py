import web
import json
import csv
from pyproj import Proj, transform
import geopy.distance
import time
urls = ("/GPSendpoint", "nearestBuilding",
		"/", "check")

class check:
	def GET(self):
		return "200 OK"


class nearestBuilding:
	def __init__(self):
		self.boroughCode = {"MN":1,
							"BX":2,
							"BK":3,
							"QN":4,
							"SI":5}
		self.coordinates = LBuildings.coordinates
		self.buildingParams = LBuildings.buildingParams
		
		# self.loadPLUTO("datasets/PLUTO_Bronx.csv", "Bronx")
		# self.loadPLUTO("datasets/PLUTO_Brooklyn.csv", "Brooklyn")
		# self.loadPLUTO("datasets/PLUTO_Queens.csv", "Queens")
		# self.loadPLUTO("datasets/PLUTO_Staten.csv", "Staten Island")

	def GET(self):
		print("Received GPS coordinate")
		start = time.time()
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		raw_data=web.data()
		data=json.loads(raw_data)
		latitude=data["lat"]
		longitude=data["lon"]
		minDist = None
		minCoords = None
		for (lat, lon) in self.coords:
			d = geopy.distance.vincenty((lat, lon), (latitude, longitude))
			if minDist is None or d.miles < minDist:
				minDist = d.miles
				minCoords = (lat, lon)
		if minCoords is not None:
			print("Found nearest building")
			(BBL, address) = self.buildingParams[minCoords]
			print((address, minDist))
		end = time.time()
		print("Finished GPS localization, " + str(end-start) + " s\n")
		return "200 OK"

	
class loadBuildings:
	def __init__(self):
		self.boroughCode = {"MN":1,
							"BX":2,
							"BK":3,
							"QN":4,
							"SI":5}
		self.coordinates = []
		self.buildingParams = {}
		print("Initializing nearest building")
		self.loadPLUTO("datasets/PLUTO_Manhattan.csv", "Manhattan")

	def loadPLUTO(self, PLUTOfile, name):
		print("Loading PLUTO " + name + " File...")
		start = time.time()
		self.loadCSV(PLUTOfile)
		end = time.time()
		print("Finished: " + str(end-start) + " s\n")

	def loadCSV(self, PLUTOfile):
		with open (PLUTOfile, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = True
			for row in reader:
				if i: #skip the first line
					i = False
					continue
				else:
					borough = row[0]
					block = row[1]
					lot = row[2]
					address = row[16]
					B = str(self.boroughCode[borough])
					if len(block) < 5:
						block = "0" * (5-len(block)) + block
					if len(lot) < 4:
						lot = "0" * (4-len(lot)) + lot
					BBL = B + block + lot
					
					xcoord = row[74]
					ycoord = row[75]
					if len(xcoord) == 0 or len(ycoord) == 0:
						continue
					lon, lat = transform(self.inProj, self.outProj, xcoord, ycoord)
					buildingCoords = (lat, lon)
					self.coords.append(buildingCoords)
					self.buildingParams[buildingCoords] = (BBL, address)
LBuildings = loadBuildings()
GPSreport = web.application(urls, locals())