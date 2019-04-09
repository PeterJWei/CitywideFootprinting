import csv
import web
import json
import datetime
import sys
import pickle
import math
from sklearn import linear_model

class estimateCensus:
	def __init__(self):
		self.boroughCode = {"MN":1,
							"BX":2,
							"BK":3,
							"QN":4,
							"SI":5}
		self.censusPop = {}
		self.censusBuildings = {}
		self.censusResArea = {}
		self.buildingList = []
		self.buildingEnergy = []
		self.loadCensusData("CensusData/NYCBlocks/Manhattan.csv")
		print("Loaded Manhattan...")
		self.loadPlutoData("datasets/PLUTO_Manhattan.csv")
		print("Loaded PLUTO Data...")
		self.estimateEnergy("estimatedEnergyPop.csv")
		#self.estimatePlutoBuildings("estimatedBuildingPop.csv")
		print("Estimated PLUTO Buildings")
		

	def loadCensusData(self, blockFile):
		with open(blockFile, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = 0
			for row in reader:
				i += 1
				if i <= 2: #skip the first 2 lines
					continue
				else:
					if i % 100 == 0:
						sys.stdout.write("\033[F")
						sys.stdout.write("\033[K")
						print("Loading Census " + str(i) + " of " + str(3952))
					GEOid2 = row[1]
					blockNumber = str(1) + GEOid2[5:] #convert GEOid2 to block number (bits 4-14)
					estimated = row[3] #estimated populations
					try:
						self.censusPop[blockNumber] = int(estimated)
					except ValueError:
						self.censusPop[blockNumber] = 0

	def loadPlutoData(self, PLUTOFile):
		with open (PLUTOFile, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = 0
			for row in reader:
				i += 1 
				if i <= 1: #skip the first line
					continue
				else:
					if i % 100 == 0:
						sys.stdout.write("\033[F")
						sys.stdout.write("\033[K")
						print("Loading Census " + str(i) + " of " + str(42967))
					borough = row[0]
					bloc = row[1]
					lot = row[2]
					resarea = float(row[36])
					CT2010 = row[4]
					CB2010 = row[5]
					if len(CT2010) == 0 or len(CB2010) != 4:
						continue
					CT2010Split = CT2010.split(".")
					if len(CT2010Split) == 1:
						tract = CT2010Split[0]
						CT2010 = "0" * (4-len(tract)) + tract + "00"
					elif len(CT2010Split) == 2:
						tract = CT2010Split[0]
						subtract = CT2010Split[1]
						CT2010 = "0" * (4-len(tract)) + tract + "0"*(2-len(subtract)) + subtract
					block = str(1) + str(CT2010) + str(CB2010)
					(totalArea, residential, office, retail, garage,
						storage, factory) = (0,0,0,0,0,0,0)
					try:
						totalArea = float(row[34])
						commercial = float(row[35])/totalArea
						residential = float(row[36])/totalArea
						office = float(row[37])/totalArea
						retail = float(row[38])/totalArea
						garage = float(row[39])/totalArea
						storage = float(row[40])/totalArea
						factory = float(row[41])/totalArea
						other = float(row[42])/totalArea
						totalArea = math.log(totalArea)
					except Exception as e:
						continue
					year = row[61]
					(YB0, YB1, YB2, YB3, YB4) = (0,0,0,0,0)
					if year <= 1930:
						YB0 = 1
					elif year > 1930 and year <= 1950:
						YB1 = 1
					elif year > 1950 and year <= 1970:
						YB2 = 1
					elif year > 1970 and year <= 1990:
						YB3 = 1
					else:
						YB4 = 1


					self.buildingList.append(["MN", bloc, lot])
					self.buildingEnergy.append([1,0,0,0,0,45,44,46,53.2, 52.2, 54.2,totalArea,
						YB0,YB1,YB2,YB3,YB4,commercial, residential, office, retail, garage, storage, factory, other])
					if block in self.censusPop:
						if block not in self.censusBuildings:
							self.censusBuildings[block] = []
							self.censusResArea[block] = 0
						self.censusBuildings[block].append(("MN",bloc,lot,resarea))
						self.censusResArea[block] += resarea

	def estimateEnergy(self, filename):
		filename2 = 'energyModels/NYCHARegressionModel.sav'
		self.model = pickle.load(open(filename2, 'rb'))
		# #self.baseData[['Manhattan', 'Brooklyn', 'Queens', 'Bronx',
		# #			'Staten', 'DPmax', 'DPmin', 'DPavg', 'DBmax', 'DBmin', 'DBavg',
		# 			'totalArea', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'commercial', 'residential', 'office',
		# 			'retail', 'garage', 'storage', 'factory', 'other']]
		self.predictions = self.model.predict(self.buildingEnergy)
		self.power = []
		for i in range(len(self.predictions)):
			self.power.append(math.exp(self.predictions[i][0])/720)


		print(len(self.predictions[0]))
		with open(filename, 'wb') as csvfile:
			csvwriter = csv.writer(csvfile, delimiter=',')
			csvwriter.writerow(["Borough", "Block", "Lot", "Population"])
			for i,(borough,block,lot) in enumerate(self.buildingList):
				csvwriter.writerow([borough,block,lot,self.power[i]])

	def estimatePlutoBuildings(self, filename):
		with open(filename, 'wb') as csvfile:
			csvwriter = csv.writer(csvfile, delimiter=',')
			csvwriter.writerow(["Borough", "Block", "Lot", "Population"])
			i = 0
			numBuildings = len(self.censusBuildings)
			for block in self.censusBuildings:
				i += 1
				if i % 1000 == 0:
						sys.stdout.write("\033[F")
						sys.stdout.write("\033[K")
						print("Loading Census " + str(i) + " of " + str(numBuildings))
				BBLs = self.censusBuildings[block]
				l = len(BBLs)
				if (l == 0):
					continue
				totalArea = self.censusResArea[block]
				if totalArea <= 1:
					continue
				pop = self.censusPop[block]
				for BBL in BBLs:
					(borough, bloc, lot, resarea) = BBL
					csvwriter.writerow([borough, bloc, lot, int(round(pop*resarea/totalArea))])

estimateCensus()


