import web
import json
import csv
from pyproj import Proj, transform
import geopy.distance
import time
import pickle
from sklearn import linear_model 
import math
import energyServer
from energyModels import dailyInterpolation
from datetime import datetime
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
		self.model = LBuildings.model
		self.referenceModels = LBuildings.referenceModels
		self.totals = LBuildings.totals
		
		# self.loadPLUTO("datasets/PLUTO_Bronx.csv", "Bronx")
		# self.loadPLUTO("datasets/PLUTO_Brooklyn.csv", "Brooklyn")
		# self.loadPLUTO("datasets/PLUTO_Queens.csv", "Queens")
		# self.loadPLUTO("datasets/PLUTO_Staten.csv", "Staten Island")

	def POST(self):
		print("############### START SUMMARY #############\nReceived GPS coordinate")
		start = time.time()
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		raw_data=web.data()
		coords = raw_data.split(',')
		#data=json.loads(raw_data)
		latitude=float(coords[0])
		longitude=float(coords[1])
		minDist = None
		minCoords = None

		month = datetime.now().month-1

		for (lat, lon) in self.coordinates:
			d = geopy.distance.vincenty((lat, lon), (latitude, longitude))
			if minDist is None or d.miles < minDist:
				minDist = d.miles
				minCoords = (lat, lon)
		if minCoords is not None:
			print("Found nearest building")
			
			# Get the closest building
			(address, MN, BK, QN, BX, SI,
			totalArea, YB0, YB1, YB2, YB3, YB4, residential, office, retail,
			garage, storage, factory) = self.buildingParams[minCoords]
			
			datapoint = [[MN, BK, QN, BX, SI, 24, 20, 22, 51, 34, 42, totalArea,
			YB0, YB1, YB2, YB3, YB4, residential, office, retail, garage, storage, factory]]
			print(address)
			print(datapoint[0])


			# Get energy prediction
			prediction = self.model.predict(datapoint)[0][0]
			print(str(math.exp(prediction)) + " kWh")
			resFrac = self.totals['MidriseApartment'][month]*residential
			offFrac = self.totals['LargeOffice'][month]*office
			retFrac = self.totals['Stand-aloneRetail'][month]*retail
			garFrac = self.totals['Warehouse'][month]*garage
			stoFrac = self.totals['Warehouse'][month]*storage
			facFrac = self.totals['Warehouse'][month]*factory
			referenceTotal = resFrac + offFrac + retFrac + garFrac + stoFrac + facFrac
			scaling = 1.0
			if abs(referenceTotal) < 10:
				scaling = 1.0
			else:
				scaling = math.exp(prediction)/referenceTotal
			#########################
			
			# get hours since Jan 1
			dt = datetime.now()
			st = datetime(2019, 1, 1, 1)
			index = int((dt - st).total_seconds()/3600)
			print("Hours since start of year: " + str(index))
			# get power prediction
			resPow = self.referenceModels['MidriseApartment'][index]*residential
			offPow = self.referenceModels['LargeOffice'][index]*office
			retPow = self.referenceModels['Stand-aloneRetail'][index]*retail
			garPow = self.referenceModels['Warehouse'][index]*garage
			stoPow = self.referenceModels['Warehouse'][index]*storage
			facPow = self.referenceModels['Warehouse'][index]*factory
			powerPrediction = resPow + offPow + retPow + garPow + stoPow + facPow # get prediction
			powerPrediction = scaling*powerPrediction
			print("Power Consumption: " + str(powerPrediction) + " kW")

			energyServer.db.recordCoordinates("fe937490cb3a36a1", latitude, longitude)
		
		end = time.time()
		print("Finished GPS localization, " + str(end-start) + " s\n")
		print("############### END SUMMARY #############")
		return "200 OK"

	
class loadBuildings:
	def __init__(self):
		self.referenceModels = dailyInterpolation.I.footprints
		self.totals = dailyInterpolation.I.totals
		self.boroughCode = {"MN":1,
							"BX":2,
							"BK":3,
							"QN":4,
							"SI":5}
		self.inProj = Proj(init='epsg:2263', preserve_units=True)
		self.outProj = Proj(init='epsg:4326')
		self.coordinates = []
		self.buildingParams = {}
		filename = 'dynamicData/NYCHARegressionModel.sav'
		self.model = pickle.load(open(filename, 'rb'))
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
					B = self.boroughCode[borough]
					(MN, BK, QN, BX, SI) = (0,0,0,0,0)
					if B == 1:
						MN = 1
					elif B == 2:
						BX = 1
					elif B == 3:
						BK = 1
					elif B == 4:
						QN = 1
					else:
						SI = 1
					B = str(B)
					(totalArea, residential, office, retail, garage,
						storage, factory) = (0,0,0,0,0,0,0)
					try:
						totalArea = float(row[34])
						residential = float(row[36])/totalArea
						office = float(row[37])/totalArea
						retail = float(row[38])/totalArea
						garage = float(row[39])/totalArea
						storage = float(row[40])/totalArea
						factory = float(row[41])/totalArea
						totalArea = math.log(totalArea)
					except Exception as e:
						continue
					year = row[61]
					(YB0, YB1, YB2, YB3, YB4) = (0,0,0,0,0)
					if year <= 1930:
						YB0 = 1
					elif year > 1930 and year <= 1950:
						YB1 = 1
					elif year > 1950 and year <= 1970:
						YB2 = 1
					elif year > 1970 and year <= 1990:
						YB3 = 1
					else:
						YB4 = 1
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
					self.coordinates.append(buildingCoords)
					self.buildingParams[buildingCoords] = (address, MN, BK, QN, BX, SI,
						totalArea, YB0, YB1, YB2, YB3, YB4, residential, office, retail,
						garage, storage, factory)
LBuildings = loadBuildings()
GPSreport = web.application(urls, locals())