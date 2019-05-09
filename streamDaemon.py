from threading import Thread
import time
import pickle
from Remote2StopID import remoteDictionary
from subwayStream import subwayStream
import datetime
import CarCounting.getDOTstream as D


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
		self.totalChanges = {}
		self.tempChanges = {}
		self.totalChangesList = []
		self.V = D.vehicleCount()
		self.currentVehicleChanges = {}
		self.cameraDictionary = self.load_obj("camera2buildings")
		self.vehicleChangesList = []

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
			self.currentVehicleChanges[797] = self.V.vehicleCountFromImage()
			self.vehicleChanges()

	def clearList(self):
		self.buildingChanges = {}
		self.buildingChangesList = []
		self.dynamicChanges = []
		self.tempChanges = {}

	def vehicleChanges(self):
		print("\nVehicle Information\n--------------")
		for camera in [797]:
			numBuildings = len(self.cameraDictionary[camera])
			diff = self.currentVehicleChanges[camera]*1000.0/numBuildings
			for (Borough, Block, Lot, ratioOffice, ratioRetail, ratioResidential, dist) in self.cameraDictionary[camera]:
				self.vehicleChangesList.append((Borough, Block, Lot, diff))

	def subwayChanges(self):
		print("\nStation Information\n--------------")
		stationTrains = self.MTAstream.getData(0x1FF)
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
			diff = (exitDiff-entryDiff)#/numBuildings
			#for (Borough, Block, Lot, comArea, resArea, offArea, retArea, dist) in self.stationDictionary[station]:
			for (Borough, Block, Lot, ratioOffice, ratioRetail, ratioResidential, dist) in self.stationDictionary[station]:
				addedPop = 0
				now = datetime.datetime.now()
				hour = now.hour
				if hour > 14 or hour < 5:
					addedPop = exitDiff*ratioResidential - entryDiff*(ratioOffice*0.616 + ratioRetail*0.297)
				else:
					addedPop = exitDiff*(ratioOffice*0.616 + ratioRetail*0.297) - entryDiff*(ratioResidential)
				if (Borough, Block, Lot) in self.buildingChanges:
					self.buildingChanges[(Borough, Block, Lot)] += addedPop
				else:
					self.buildingChanges[(Borough, Block, Lot)] = addedPop
				if (Borough, Block, Lot) in self.totalChanges:
					self.totalChanges[(Borough, Block, Lot)] += addedPop
				else:
					self.totalChanges[(Borough, Block, Lot)] = addedPop
				self.tempChanges[(Borough, Block, Lot)] = self.totalChanges[(Borough, Block, Lot)]
		for BBL in self.tempChanges:
			(borough, block, lot) = BBL
			try:
				diff = self.buildingChanges[BBL]
				self.totalChangesList.append((borough, block, lot, diff))
			except KeyError:
				continue

		for BBL in self.buildingChanges:
			(borough, block, lot) = BBL
			try:
				diff = self.buildingChanges[BBL]
				self.buildingChangesList.append((borough, block, lot, diff))
				self.dynamicChanges.append((self.convert2BBL(borough,str(block),str(lot)),diff))
				
			except KeyError:
				continue
		print("Total trains stopped: " + str(totalTrains))
		#print(len(self.buildingChangesList))
		print("End Station Information")

	def convert2BBL(self, borough, block, lot):
		B1 = "0"
		if borough in self.boroughCode:
			B1 = str(self.boroughCode[borough])
		d1 = len(block)
		d2 = len(lot)
		return B1 + "0"*(5-d1) + block + "0"*(4-d2) + lot





