from threading import Thread
import time
import pickle
from Remote2StopID import remoteDictionary
from subwayStream import subwayStream



class streams:
	def __init__(self):
		self.checkInterval = 30
		self.startDaemon()
		self.boroughCode = {"MN":1,
							"BX":2,
							"BK":3,
							"QN":4,
							"SI":5}
		self.stationDictionary = self.load_obj("station2buildings")
		print("Pickle Loaded " + 'station2buildings.pkl')
		self.MTAstream = subwayStream()
		print("MTA Stream Loaded")
		S = remoteDictionary()
		self.timeSeriesEntries = S.timeSeriesDataEntries
		self.timeSeriesExits = S.timeSeriesDataExits
		print("Time Series Datapoints: " + str(len(self.timeSeriesEntries)))
		self.buildingChanges = {}
		self.buildingChangesList = []
		self.dynamicChanges = []
		self.hello = "Hello World!\n\n\n\n\n\n\n"

	def load_obj(self, name):
		with open('obj/' + name + '.pkl', 'rb') as f:
			return pickle.load(f)

	def startDaemon(self):
		t=Thread(target=self._loopCheckStreams, args=())
		t.setDaemon(True)
		t.start()

	def _loopCheckStreams(self):
		while True:
			time.sleep(self.checkInterval)
			self.subwayChanges()

	def clearList(self):
		self.buildingChanges = {}
		self.buildingChangesList = []
		self.dynamicChanges = []

	def subwayChanges(self):
		print("\nStation Information\n--------------")
		stationTrains = self.MTAstream.getData(0x1)
		#for station in stationTrains:
		#	print(str(stationTrains[station]) + " trains passed station: " + station)
		t = 1
		totalTrains = 0
		for station in stationTrains:
			#Trainslate s to station
			#TODO
			totalTrains += stationTrains[station]
			#print(str(stationTrains[station]) + " trains passed station: " + station)
			if station not in self.stationDictionary or station not in self.timeSeriesEntries:
				print("No station: " + str(station) + " found")
				continue
			entryDiff = self.timeSeriesEntries[station][t] - self.timeSeriesEntries[station][t-1]
			exitDiff = self.timeSeriesExits[station][t] - self.timeSeriesExits[station][t-1]

			if entryDiff > 100000 or exitDiff > 100000 or entryDiff < -100000 or exitDiff < -100000:
				continue
			numBuildings = len(self.stationDictionary[station])
			if numBuildings == 0:
				continue
			diff = (exitDiff-entryDiff)/numBuildings
			for (Borough, Block, Lot, dist) in self.stationDictionary[station]:
				if (Borough, Block, Lot) in self.buildingChanges:
					self.buildingChanges[(Borough, Block, Lot)] += diff
				else:
					self.buildingChanges[(Borough, Block, Lot)] = diff
		self.buildingChangesList = []
		for BBL in self.buildingChanges:
			(borough, block, lot) = BBL
			diff = self.buildingChanges[BBL]
			self.buildingChangesList.append((borough, block, lot, diff))
			self.dynamicChanges.append((self.convert2BBL(borough,str(block),str(lot)),diff))
		print("Total trains stopped: " + str(totalTrains))
		#print(len(self.buildingChangesList))
		print("End Station Information")

	def convert2BBL(self, borough, block, lot):
		B1 = "0"
		if borough in self.boroughCode:
			B1 = self.boroughCode[borough]
		d1 = len(block)
		d2 = len(lot)
		return B1 + "0"*(5-d1) + block + "0"*(4-d2) + lot





