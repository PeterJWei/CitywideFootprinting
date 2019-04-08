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
		self.coordinates = energyServer.LBuildings.coordinates
		self.buildingParams = energyServer.LBuildings.buildingParams
		self.model = energyServer.LBuildings.model
		self.referenceModels = energyServer.LBuildings.referenceModels
		self.totals = energyServer.LBuildings.totals
		self.BBL2CT = energyServer.LBuildings.BBL2CT
		self.CT2BBL = energyServer.LBuildings.CT2BBL
		self.BBLpopulation = energyServer.LBuildings.BBLpopulation
		self.PopulationDictionary = LPopulation.PopulationDictionary
		
		# self.loadPLUTO("datasets/PLUTO_Bronx.csv", "Bronx")
		# self.loadPLUTO("datasets/PLUTO_Brooklyn.csv", "Brooklyn")
		# self.loadPLUTO("datasets/PLUTO_Queens.csv", "Queens")
		# self.loadPLUTO("datasets/PLUTO_Staten.csv", "Staten Island")

	def POST(self):
		print("\n############### START SUMMARY #############\nReceived GPS coordinate")
		print("Number of building changes" + str(len(energyServer.S.buildingChangesList)))
		start = time.time()
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		raw_data=web.data()
		dat = raw_data.split(',')
		#data=json.loads(raw_data)
		userID = dat[0]
		latitude=float(dat[1])
		longitude=float(dat[2])
		accuracy = float(dat[3])
		speed=float(dat[4])
		course=float(dat[5])
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
			(BBL, address, MN, BK, QN, BX, SI,
			totalArea, YB0, YB1, YB2, YB3, YB4, commercial, residential, office, retail,
			garage, storage, factory, other) = self.buildingParams[minCoords]

			CT = self.BBL2CT[BBL]
			buildingList = self.CT2BBL[CT]
			print("Number of buildings: " + str(len(buildingList)))
			totalUnits = 0
			currentUnits = 0
			for (num, units) in buildingList:
				if num == BBL:
					currentUnits = units
				totalUnits += units
			if totalUnits == 0:
				totalUnits = 1
			estimatedPopulation = self.PopulationDictionary[CT]*currentUnits/totalUnits
			print(estimatedPopulation)
			datapoint = [[MN, BK, QN, BX, SI, 24, 20, 22, 51, 34, 42, totalArea,
			YB0, YB1, YB2, YB3, YB4, commercial, residential, office, retail, garage, storage, factory, other]]
			print(address)
			print(datapoint[0])

			# Get energy prediction
			prediction = self.model.predict(datapoint)[0][0]
			print(str(math.exp(prediction)) + " kWh")
			comFrac = self.totals['LargeOffice'][month]*commercial
			resFrac = self.totals['MidriseApartment'][month]*residential
			offFrac = self.totals['LargeOffice'][month]*office
			retFrac = self.totals['Stand-aloneRetail'][month]*retail
			garFrac = self.totals['Warehouse'][month]*garage
			stoFrac = self.totals['Warehouse'][month]*storage
			facFrac = self.totals['Warehouse'][month]*factory
			othFrac = self.totals['Warehouse'][month]*other
			referenceTotal = comFrac + resFrac + offFrac + retFrac + garFrac + stoFrac + facFrac + othFrac
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
			comPow = self.referenceModels['LargeOffice'][index]*commercial
			resPow = self.referenceModels['MidriseApartment'][index]*residential
			offPow = self.referenceModels['LargeOffice'][index]*office
			retPow = self.referenceModels['Stand-aloneRetail'][index]*retail
			garPow = self.referenceModels['Warehouse'][index]*garage
			stoPow = self.referenceModels['Warehouse'][index]*storage
			facPow = self.referenceModels['Warehouse'][index]*factory
			othPow = self.referenceModels['Warehouse'][index]*other
			powerPrediction = comPow + resPow + offPow + retPow + garPow + stoPow + facPow + othPow# get prediction
			powerPrediction = scaling*powerPrediction
			print("Power Consumption: " + str(powerPrediction) + " kW")
			footprint = powerPrediction
			if estimatedPopulation > 0:
				footprint = powerPrediction/estimatedPopulation
			#energyServer.db.recordCoordinates(userID, latitude, longitude, accuracy, speed, course)
			energyServer.db.recordInfo(userID, latitude, longitude, accuracy, speed, course, powerPrediction, estimatedPopulation, footprint)
		end = time.time()
		print("Finished GPS localization, " + str(end-start) + " s")
		print("############### END SUMMARY #############\n")
		ret = {
			"address":address,
			"footprint":footprint
		}
		return json.dumps(ret)

class loadPopulation:
	def __init__(self):
		self.PopulationDictionary = {}
		print("Loading Manhattan Census...")
		self.loadCensusData(1, "CensusData/NYCBlocks/Manhattan.csv")
		# self.loadCensusData(2, "CensusData/NYCBlocks/Bronx.csv")
		# self.loadCensusData(3, "CensusData/NYCBlocks/Kings.csv")
		# self.loadCensusData(4, "CensusData/NYCBlocks/Queens.csv")
		# self.loadCensusData(5, "CensusData/NYCBlocks/Richmond.csv")


	def loadCensusData(self, borough, blockFile):
		with open(blockFile, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = 0
			for row in reader:
				i += 1
				if i <= 2: #skip the first 2 lines
					continue
				else:
					GEOid2 = row[1]
					blockNumber = str(borough) + GEOid2[5:] #convert GEOid2 to block number (bits 4-14)
					estimated = row[3] #estimated populations
					assert(blockNumber not in self.PopulationDictionary)
					try:
						self.PopulationDictionary[blockNumber] = int(estimated)
					except ValueError:
						self.PopulationDictionary[blockNumber] = 0
	

LPopulation = loadPopulation()
GPSreport = web.application(urls, locals())