import csv
import web
import json
import datetime

urls = ("/energyData", "energyDataReturn",
		"/", "check")

class check:
	def GET(self):
		return "200 OK"

class energyDataClass:
	def __init__(self, borough=1):
		#web.header('Access-Control-Allow-Origin', '*')
		#web.header('Access-Control-Allow-Credentials', 'true')
		self.data = []
		self.loadEstimatedEnergy("staticData/estimatedEnergyPop.csv")
		print("Loaded Manhattan Energy...")

	def loadEstimatedEnergy(self, energyFile):
		with open(energyFile, 'rb') as csvfile:
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

	def returnEnergyEstimates(self):
		return self.data

EData = censusDataClass()

class energyDataReturn:
	def GET(self):
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		ED = EData.returnEnergyEstimates()
		return json.dumps(ED)

energyData = web.application(urls, locals());