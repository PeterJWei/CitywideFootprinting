import json
import csv
from pyproj import Proj, transform
import geopy.distance
import time
import pickle
from energyModels import dailyInterpolation
from datetime import datetime
import math
class loadBuildings:
	def __init__(self):
		self.PopulationDictionary = {}
		self.BBLpopulation = {}
		print("Loading Manhattan Census...")
		self.loadCensusData(1, "CensusData/NYCBlocks/Manhattan.csv")

		self.referenceModels = dailyInterpolation.I.footprints
		self.totals = dailyInterpolation.I.totals
		self.boroughCode = {"MN":1,
							"BX":2,
							"BK":3,
							"QN":4,
							"SI":5}
		self.inProj = Proj(init='epsg:2263', preserve_units=True)
		self.outProj = Proj(init='epsg:4326')
		self.coordinates = []
		self.buildingParams = {}
		self.BBL2CT = {}
		self.CT2BBL = {}
		
		filename = 'dynamicData/NYCHARegressionModel.sav'
		self.model = pickle.load(open(filename, 'rb'))
		print("Initializing nearest building")
		self.loadPLUTO("datasets/PLUTO_Manhattan.csv", "Manhattan")
		self.estimateBaseline()
		print("Completed Baseline Estimation")

	def loadPLUTO(self, PLUTOfile, name):
		print("Loading PLUTO " + name + " File...")
		start = time.time()
		self.loadCSV(PLUTOfile)
		end = time.time()
		print("Finished: " + str(end-start) + " s\n")

	def estimateBaseline(self):
		for CT in self.PopulationDictionary:
			blockPop = self.PopulationDictionary[CT]
			buildingList = self.CT2BBL[CT]
			totalUnits = 0
			for (BBL, units) in buildingList:
				totalUnits += units
			if totalUnits == 0:
				totalUnits = 1
			for (BBL, units) in buildingList:
				self.BBLpopulation[BBL] = blockPop*units/totalUnits

	def loadCensusData(self, borough, blockFile):
		with open(blockFile, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = 0
			for row in reader:
				i += 1
				if i <= 2: #skip the first 2 lines
					continue
				else:
					GEOid2 = row[1]
					blockNumber = str(borough) + GEOid2[5:] #convert GEOid2 to block number (bits 4-14)
					estimated = row[3] #estimated populations
					assert(blockNumber not in self.PopulationDictionary)
					try:
						self.PopulationDictionary[blockNumber] = int(estimated)
					except ValueError:
						self.PopulationDictionary[blockNumber] = 0

	def loadCSV(self, PLUTOfile):
		with open (PLUTOfile, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = True
			for row in reader:
				if i: #skip the first line
					i = False
					continue
				else:
					borough = row[0]
					block = row[1]
					lot = row[2]
					CT2010 = row[4]
					CB2010 = row[5]
					
					if len(CT2010) == 0 or len(CB2010) != 4 or borough not in self.boroughCode:
						continue
					CT2010Split = CT2010.split(".")
					if len(CT2010Split) == 1:
						tract = CT2010Split[0]
						CT2010 = "0" * (4-len(tract)) + tract + "00"
					elif len(CT2010Split) == 2:
						tract = CT2010Split[0]
						subtract = CT2010Split[1]
						CT2010 = "0" * (4-len(tract)) + tract + "0"*(2-len(subtract)) + subtract
					CTblock = str(self.boroughCode[borough]) + str(CT2010) + str(CB2010)

					address = row[16]
					B = self.boroughCode[borough]
					(MN, BK, QN, BX, SI) = (0,0,0,0,0)
					if B == 1:
						MN = 1
					elif B == 2:
						BX = 1
					elif B == 3:
						BK = 1
					elif B == 4:
						QN = 1
					else:
						SI = 1
					B = str(B)
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

						resUnits = float(row[46])
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
					if len(block) < 5:
						block = "0" * (5-len(block)) + block
					if len(lot) < 4:
						lot = "0" * (4-len(lot)) + lot
					BBL = B + block + lot
					
					self.BBL2CT[BBL] = CTblock
					self.BBLpopulation[BBL] = 0
					if CTblock not in self.BBL2CT:
						self.CT2BBL[CTblock] = []
					self.CT2BBL[CTblock].append((BBL,resUnits))
					
					xcoord = row[74]
					ycoord = row[75]
					if len(xcoord) == 0 or len(ycoord) == 0:
						continue
					lon, lat = transform(self.inProj, self.outProj, xcoord, ycoord)
					buildingCoords = (lat, lon)
					self.coordinates.append(buildingCoords)
					self.buildingParams[buildingCoords] = (BBL, address, MN, BK, QN, BX, SI,
						totalArea, YB0, YB1, YB2, YB3, YB4, commercial, residential, office, retail,
						garage, storage, factory, other)

