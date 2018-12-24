import csv
import web
import json
import datetime

urls = ("/censusData", "censusDataReturn",
		"/", "check")

class check:
	def GET(self):
		return "200 OK"

class censusDataClass:
	def __init__(self, borough=1):
		#web.header('Access-Control-Allow-Origin', '*')
		#web.header('Access-Control-Allow-Credentials', 'true')
		self.data = []
		self.loadEstimatedCensus("staticData/estimatedBuildingPop.csv")
		print("Loaded Manhattan Census...")

	def loadEstimatedCensus(self, popFile):
		with open(popFile, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = 0
			for row in reader:
				i += 1
				if i <= 1: #skip the first 2 lines
					continue
				else:
					borough = row[0]
					block = row[1]
					lot = row[2]
					pop = row[3]
					self.data.append([borough, block, lot, pop])

	def returnCensusEstimates(self):
		return self.data

CData = censusDataClass()

class censusDataReturn:
	def GET(self):
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		CD = CData.returnCensusEstimates()
		return json.dumps(CD)

censusData = web.application(urls, locals());