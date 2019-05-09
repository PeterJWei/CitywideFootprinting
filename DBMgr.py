import pymongo
import datetime
import time
import csv
import math


class DBMgr(object):
	def __init__(self, start_bg_thread=True):
		self.dbc=pymongo.MongoClient()
		db1 = self.dbc.test_database
		self.coords = db1.GPSData
		self.state = db1.stateInformation

	def recordFullState(self, energy, population):
		self.state.insert({
			"timestamp": datetime.datetime.now(),
			"energy": energy,
			"population": population
			})

	def recordStateInformation(self, traffic, subway, weather):
		self.state.insert({
			"timestamp": datetime.datetime.now(),
			"subway": subway,
			"traffic": traffic,
			"weather": weather
			})

	def recordCoordinates(self, user, lat, lon, accuracy, speed, course):
		self.coords.insert({
			"timestamp": datetime.datetime.now(),
			"user": user,
			"lat": lat,
			"lon": lon,
			"accuracy": accuracy,
			"speed": speed,
			"course": course
			})

	def recordInfo(self, user, lat, lon, accuracy, speed, course, mode, energy, population, footprint):
		self.coords.insert({
			"timestamp": datetime.datetime.now(),
			"user": user,
			"lat": lat,
			"lon": lon,
			"accuracy": accuracy,
			"speed": speed,
			"course": course,
			"mode": mode,
			"energy": energy,
			"population": population,
			"footprint": footprint
			})
	#"fe937490cb3a36a1"
	#"45458C82-9CE4-412F-8BD7-0D45CA175508"

	def retrieveStateParameters(self, start, end):
		ret = []
		conditions = {
			"timestamp":{
				"$gte":datetime.datetime.utcfromtimestamp(start),
				"$lt":datetime.datetime.utcfromtimestamp(end)
			}
		}
		iterator = self.state.find().sort([("timestamp", pymongo.ASCENDING)])

	def pullCoordinates(self, user):
		ret = []
		conditions = {
			"user": user
		}
		iterator = self.coords.find(conditions).sort([("timestamp", pymongo.ASCENDING)])
		for datapoint in iterator:
			ret.append((datapoint["timestamp"], datapoint["lat"], datapoint["lon"], datapoint["speed"]))
		with open("GPScoordinates.csv", 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			writer.writerow(['timestamp', 'latitude', 'longitude', 'speed'])
			for coord in ret:
				writer.writerow([coord[0], coord[1], coord[2], coord[3]])

	def getEnergyFootprint(self, user):
		ret = []
		conditions = {
			"user": user
		}		
		iterator = self.coords.find(conditions).sort([("timestamp", pymongo.ASCENDING)])
		for datapoint in iterator:
			if "footprint" in datapoint:
				ret.append((datapoint["timestamp"], datapoint["footprint"]))
		return ret

	def energyDictionary(self, model, buildingParameters, totals, reference):
		ret = {}
		month = datetime.datetime.now().month-1
		for coords in buildingParameters:
			(BBL, address, MN, BK, QN, BX, SI,
			totalArea, YB0, YB1, YB2, YB3, YB4, commercial, residential, office, retail,
			garage, storage, factory, other) = buildingParameters[coords]
			datapoint = [[MN, BK, QN, BX, SI, 24, 20, 22, 51, 34, 42, totalArea,
			YB0, YB1, YB2, YB3, YB4, commercial, residential, office, retail, garage, storage, factory, other]]
			# Get energy prediction
			prediction = model.predict(datapoint)[0][0]
			print(str(math.exp(prediction)) + " kWh")
			comFrac = totals['LargeOffice'][month]*commercial
			resFrac = totals['MidriseApartment'][month]*residential
			offFrac = totals['LargeOffice'][month]*office
			retFrac = totals['Stand-aloneRetail'][month]*retail
			garFrac = totals['Warehouse'][month]*garage
			stoFrac = totals['Warehouse'][month]*storage
			facFrac = totals['Warehouse'][month]*factory
			othFrac = totals['Warehouse'][month]*other
			referenceTotal = comFrac + resFrac + offFrac + retFrac + garFrac + stoFrac + facFrac + othFrac
			scaling = 1.0
			if abs(referenceTotal) < 10:
				scaling = 1.0
			else:
				scaling = math.exp(prediction)/referenceTotal
			#########################
			
			# get hours since Jan 1
			dt = datetime.datetime.now()
			st = datetime.datetime(2019, 1, 1, 1)
			index = int((dt - st).total_seconds()/3600)
			print("Hours since start of year: " + str(index))
			# get power prediction
			comPow = reference['LargeOffice'][index]*commercial
			resPow = reference['MidriseApartment'][index]*residential
			offPow = reference['LargeOffice'][index]*office
			retPow = reference['Stand-aloneRetail'][index]*retail
			garPow = reference['Warehouse'][index]*garage
			stoPow = reference['Warehouse'][index]*storage
			facPow = reference['Warehouse'][index]*factory
			othPow = reference['Warehouse'][index]*other
			powerPrediction = comPow + resPow + offPow + retPow + garPow + stoPow + facPow + othPow# get prediction
			powerPrediction = scaling*powerPrediction
			print("Power Consumption: " + str(powerPrediction) + " kW")
			ret[BBL] = powerPrediction
		return ret








