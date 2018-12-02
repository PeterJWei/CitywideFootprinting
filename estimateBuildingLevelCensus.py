import csv
import web
import json
import datetime
import sys
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
		self.loadCensusData("CensusData/NYCBlocks/Manhattan.csv")
		print("Loaded Manhattan...")
		self.loadPlutoData("datasets/PLUTO_Manhattan.csv")
		print("Loaded PLUTO Data...")
		self.estimatePlutoBuildings("estimatedBuildingPop.csv")
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
					if block in self.censusPop:
						if block not in self.censusBuildings:
							self.censusBuildings[block] = []
							self.censusResArea[block] = 0
						self.censusBuildings[block].append(("MN",bloc,lot,resarea))
						self.censusResArea[block] += resarea


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


