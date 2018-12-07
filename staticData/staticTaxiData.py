import csv
import web
import json
import datetime

urls = ("/taxiOriginData", "taxiOrigin",
	"/taxiDestinationData", "taxiDestination",
	"/", "check")


class check:
	def GET(self):
		return "200 OK"

class dataClass:
	def __init__(self):
		self.taxiOriginData = self.loadTimeSeriesData("staticData/TaxiOriginBBL.csv")
		self.taxiDestinationData = self.loadTimeSeriesData("staticData/TaxiDestinationBBL.csv")
		print("\nData Class Initialized, \n" + str(len(self.taxiOriginData)))

	def loadTimeSeriesData(self, dataFile):
		data = []
		for i in range(60*60):
			data.append([])
		with open (dataFile, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = True
			for row in reader:
				if i:
					i = False
					continue
				else:
					borough = row[0]
					block = row[1]
					lot = row[2]
					hour = row[3]
					minute = row[4]
					index = int(hour) * 60 + int(minute)
					data[index].append([borough, block, lot])
		return data

	def taxiPickups(self, hour, minute):
		index = int(hour) * 60 + int(minute)
		return self.taxiOriginData[index]

	def taxiDropoffs(self, hour, minute):
		index = int(hour) * 60 + int(minute)
		return self.taxiDestinationData[index]

taxiDataClass = dataClass()

def getTime():
	web.header('Access-Control-Allow-Origin', '*')
	web.header('Access-Control-Allow-Credentials', 'true')
	now = datetime.datetime.now()
	hour = now.hour
	minute = now.minute
	return (hour, minute)

class taxiDestination:
	def GET(self):
		hour, minute = getTime()
		BC = taxiDataClass.taxiDropoffs(hour, minute)
		return json.dumps(BC)

class taxiOrigin:
	def GET(self):
		hour, minute = getTime()
		BC = taxiDataClass.taxiPickups(hour, minute)
		return json.dumps(BC)

taxiData = web.application(urls, locals());