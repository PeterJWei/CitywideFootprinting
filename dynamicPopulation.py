from Remote2StopID import remoteDictionary
from buildingData import buildingData
from plotNYCblocks import plotNYCblocks
import time
import web
#from subwayStream import subwayStream

urls = ("/", "dynamicAPI")

class dynamicAPI:
	def GET(self):
		self.dynamic = showDynamicPopulation()
		print("dynamic API")
		return self.dynamic.serviceStartup()

class showDynamicPopulation:
	def __init__(self):
		return

	def init(self):
		S = remoteDictionary()
		B = buildingData()
		self.BBL2CT = B.BBL2CT
		S = subwayStream()
		self.blocks2Occupancy = {}

		print("Determining Closest Station...")
		start = time.time()
		self.nearestStation = B.closestStation(S.coordinates)
		end = time.time()
		print("Finished: " + str(end-start) + " s\n")

		print("Inverting Closest Station...")
		start = time.time()
		self.station2Blocks = B.station2Blocks()
		end = time.time()
		print("Finished: " + str(end-start) + " s\n")

		self.timeSeriesEntries = S.timeSeriesDataEntries
		self.timeSeriesExits = S.timeSeriesDataExits

	def getBlocks2Occupancy(self,t):
		self.blocks2Occupancy = {}
		count = 0
		for station in self.station2Blocks:
			blockCount = len(self.station2Blocks[station])
			for block in self.station2Blocks[station]:
				if block not in self.blocks2Occupancy:
					self.blocks2Occupancy[block] = 0
				if station in self.timeSeriesEntries:
					entryDiff = self.timeSeriesEntries[station][t] - self.timeSeriesEntries[station][t-1]
					exitDiff = self.timeSeriesExits[station][t] - self.timeSeriesExits[station][t-1]
					if entryDiff > 100000 or exitDiff > 100000 or entryDiff < 0 or exitDiff < 0:
						continue
					count += 1
					self.blocks2Occupancy[block] -= (entryDiff - exitDiff)

		print("Number of nonzero changes: " + str(count) + "/" + str(len(self.blocks2Occupancy)))

	def serviceStartup(self):
		self.P = plotNYCblocks()
		json = self.P.exampleRun3()
		print(json)
		return json

	def startup(self):
		self.P = plotNYCblocks()
		self.P.exampleRun()

	def plotDynamic(self):
		self.P.dynamicPopulation(self.blocks2Occupancy)
		self.P.examplePlot2()

	def plotBuildings(self):
		self.P = plotNYCblocks()
		self.P.buildingPlot()

dynamic = showDynamicPopulation()
dynamic.plotBuildings()

doPopulation = web.application(urls, locals());