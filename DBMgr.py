import pymongo
import datetime
import time



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