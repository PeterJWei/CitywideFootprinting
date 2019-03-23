import pymongo
import datetime
import time
import csv


class DBMgr(object):
	def __init__(self, start_bg_thread=True):
		self.dbc=pymongo.MongoClient()
		db1 = self.dbc.test_database
		self.coords = db1.GPSData

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
	#"fe937490cb3a36a1"
	#"45458C82-9CE4-412F-8BD7-0D45CA175508"
	def pullCoordinates(self, user):
		ret = []
		conditions = {
			"user": user
		}
		iterator = self.coords.find(conditions).sort([("timestamp", pymongo.DESCENDING)])
		for datapoint in iterator:
			ret.append((datapoint["timestamp"], datapoint["lat"], datapoint["lon"], datapoint["speed"]))
		with open("GPScoordinates.csv", 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			writer.writerow(['timestamp', 'latitude', 'longitude', 'speed'])
			for coord in ret:
				writer.writerow([coord[0], coord[1], coord[2], coord[3]])