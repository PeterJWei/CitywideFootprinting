import csv
import web
import json
import datetime
urls = ("/data", "FS",
	"/", "check")

class check:
	def GET(self):
		return "200 OK"
class dataClass:
	def __init__(self):
		self.timeData = []
		for i in range(60*60):
			self.timeData.append([])
		assert(len(self.timeData) == 60*60)
		self.loadCheckinData("staticData/BBLData.csv")
		print("\nFoursquare Data Class Initialized, \n" + str(len(self.timeData)))

	def loadCheckinData(self, dataFile):
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
					self.timeData[index].append([borough, block, lot])

	def buildingCheckins(self, hour, minute):
		index = int(hour) * 60 + int(minute)
		return self.timeData[index]

FSData = dataClass()

class FS:
	def GET(self):
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		now = datetime.datetime.now()
		hour = now.hour
		minute = now.minute
		BC = FSData.buildingCheckins(hour, minute)
		j = json.dumps(BC)
		print(j)
		return json.dumps(BC)#"runDynamic(" + json.dumps(BC) + ");"

foursquareData = web.application(urls, locals());