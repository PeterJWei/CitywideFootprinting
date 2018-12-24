import csv
import web
import json
import datetime
urls = ("/checkinData", "FScheckin",
	#"/taxiOriginData", "FSorigin",
	#"/taxiDestinationData", "FSdestination",
	"/", "check")

class check:
	def GET(self):
		return "200 OK"
class dataClass:
	def __init__(self):
		self.timeData = self.loadTimeSeriesData("staticData/BBLData.csv")
		#self.taxiOriginData = self.loadTimeSeriesData("staticData/TaxiOriginBBL.csv")
		#self.taxiDestinationData = self.loadTimeSeriesData("staticData/TaxiDestinationBBL.csv")
		print("\nData Class Initialized, \n" + str(len(self.timeData)))

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

	def buildingCheckins(self, hour, minute):
		index = int(hour) * 60 + int(minute)
		return self.timeData[index]

	# def taxiPickups(self, hour, minute):
	# 	index = int(hour) * 60 + int(minute)
	# 	return self.taxiOriginData[index]

	# def taxiDropoffs(self, hour, minute):
	# 	index = int(hour) * 60 + int(minute)
	# 	return self.taxiDestinationData[index]

FSData = dataClass()

def getTime():
	web.header('Access-Control-Allow-Origin', '*')
	web.header('Access-Control-Allow-Credentials', 'true')
	now = datetime.datetime.now()
	hour = now.hour
	minute = now.minute
	return (hour, minute)

# class FSdestination:
# 	def GET(self):
# 		hour, minute = getTime()
# 		BC = FSData.taxiPickups(hour, minute)
# 		return json.dumps(BC)

# class FSorigin:
# 	def GET(self):
# 		hour, minute = getTime()
# 		BC = FSData.taxiPickups(hour, minute)
# 		return json.dumps(BC)

class FScheckin:
	def GET(self):
		hour, minute = getTime()
		BC = FSData.buildingCheckins(hour, minute)
		return json.dumps(BC)#"runDynamic(" + json.dumps(BC) + ");"

foursquareData = web.application(urls, locals());