import pymongo
import datetime
import time
import csv


class DBMgr(object):
	def __init__(self, start_bg_thread=True):
		self.dbc=pymongo.MongoClient()
		db1 = self.dbc.test_database
		self.coords = db1.coordCollection

	def recordCoordinates(self, user, lat, lon):
		self.coords.insert({
			"timestamp": datetime.datetime.now(),
			"user": user,
			"lat": lat,
			"lon": lon
			})
	#"fe937490cb3a36a1"
	def pullCoordinates(self, user):
		ret = []
		conditions = {
			"user": user
		}
		iterator = self.coords.find(conditions).sort([("timestamp", pymongo.DESCENDING)])
		for datapoint in iterator:
			ret.append((datapoint["lat"], datapoint["lon"]))
		with open("GPScoordinates.csv", 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			writer.writerow(['latitude', 'longitude'])
			for coord in ret:
				writer.writerow([coord[0], coord[1]])