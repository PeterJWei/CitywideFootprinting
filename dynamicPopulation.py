from Remote2StopID import remoteDictionary
from buildingData import buildingData
from plotNYCblocks import plotNYCblocks
from loadEnergy import loadEnergy
import time
import web
from subwayStream import subwayStream

urls = ("/", "dynamicAPI")

class dynamicAPI:
	def GET(self):
		self.dynamic = showDynamicPopulation()
		print("dynamic API")
		return self.dynamic.serviceStartup()

class showDynamicPopulation:
	def __init__(self, borough=0): # borough options: 0, all boroughs; 1, Manhattan
		self.init(borough)
		self.borough = borough
		return

	def init(self, borough=0):
		self.MTAstream = subwayStream()
		E = loadEnergy()
		self.energyDictionary = E.energyDictionary
		S = remoteDictionary()
		B = buildingData()
		self.BBL2CT = B.BBL2CT
		self.CT2EUI()
		#S = subwayStream()
		self.blocks2Occupancy = {}

		boroughFileName = {0:"AllBoroughs",
						   1:"Manhattan",
						   2:"Bronx",
						   3:"Brooklyn",
						   4:"Queens",
						   5:"Staten Island"}
		print("Determining Closest Station...")
		start = time.time()
		self.nearestStation = B.closestStation(S.coordinates, borough, boroughFileName[borough])
		end = time.time()
		print("Finished: " + str(end-start) + " s\n")

		print("Inverting Closest Station...")
		start = time.time()
		self.station2Blocks = B.station2Blocks()
		end = time.time()
		print("Finished: " + str(end-start) + " s\n")

		self.timeSeriesEntries = S.timeSeriesDataEntries
		self.timeSeriesExits = S.timeSeriesDataExits

	def CT2EUI(self):
		self.CTEUI = {}
		for BBL in self.energyDictionary:
			if BBL in self.BBL2CT:
				block = self.BBL2CT[BBL]
				if block not in self.CTEUI:
					self.CTEUI[block] = 0.0
				self.CTEUI[block] += self.energyDictionary[BBL]

	def getBlocks2Occupancy(self,t):
		self.blocks2Occupancy = {}
		stationTrains = self.MTAstream.getData(0x1FF)
		for station in stationTrains:
			print(str(stationTrains[station]) + " trains passed station: " + station)
		count = 0
		for station in stationTrains:
			#Trainslate s to station
			#TODO
			if station not in self.station2Blocks:
				#print("No station: " + str(station) + " found")
				continue
		#for station in self.station2Blocks:
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
					self.blocks2Occupancy[block] += (exitDiff - entryDiff)/blockCount/48

		print("Number of nonzero changes: " + str(count) + "/" + str(len(self.blocks2Occupancy)))

	def plotRealtime(self):
		self.P = plotNYCblocks(self.CTEUI, self.borough)
		self.P.examplePlotRealTime(self.blocks2Occupancy)

	def startup(self):
		self.P = plotNYCblocks(self.CTEUI, self.borough)
		self.P.testRun()
		#self.P.exampleRun()

	def plotDynamic(self):
		self.P = plotNYCblocks(self.CTEUI, self.borough)
		self.P.dynamicPopulation(self.blocks2Occupancy)
		self.P.examplePlot2()

doPopulation = web.application(urls, locals());