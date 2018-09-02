import csv
import time
from pyproj import Proj, transform
import geopy.distance
import sys

class buildingData:
	def __init__(self):
		self.boroughCode = {"MN":1}
		self.BBL2CT = {}
		self.inProj = Proj(init='epsg:2263', preserve_units=True)
		self.outProj = Proj(init='epsg:4326')
		print("Loading PLUTO Manhattan File...")
		start = time.time()
		self.loadCSV("datasets/PLUTO_Manhattan.csv")
		end = time.time()
		print("Finished: " + str(end-start) + " s\n")
		return

	def loadCSV(self, PLUTOfile):
		self.block2building = {}
		self.BBL2CT = {}
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
					B = str(self.boroughCode[borough])
					if len(block) < 5:
						block = "0" * (5-len(block)) + block
					if len(lot) < 4:
						lot = "0" * (4-len(lot)) + lot
					BBL = B + block + lot
					CT2010 = row[4]
					CB2010 = row[5]
					block = str(self.boroughCode[borough]) + str(CT2010) + str(CB2010)
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
					block = str(self.boroughCode[borough]) + str(CT2010) + str(CB2010)
					xcoord = row[74]
					ycoord = row[75]
					if len(xcoord) == 0 or len(ycoord) == 0:
						continue
					lon, lat = transform(self.inProj, self.outProj, xcoord, ycoord)

					#match latlon to nearest subway

					if block not in self.block2building:
						self.block2building[block] = []
					self.block2building[block].append((lat,lon))
					self.BBL2CT[BBL] = block

	def closestStation(self, stationCoordinates):
		self.nearestStationDictionary = {}
		totalBlocks = len(self.block2building)
		blockNo = 0
		for block in self.block2building:
			blockNo += 1
			if blockNo % (totalBlocks/100) == 0:
				sys.stdout.write("\033[F")
				sys.stdout.write("\033[K")
				print(str(int(round(float(blockNo)/float(totalBlocks)*100))) + "%...")
			if block[0] != "1":
				continue
			coord1 = self.block2building[block][0]
			distance = None
			closestStation = None
			for station in stationCoordinates:
				coord2 = stationCoordinates[station]
				d = geopy.distance.vincenty(coord1, coord2).miles
				#print((coord1, coord2))
				if distance is None or d < distance:
					distance = d
					closestStation = station
			#print(distance)
			if distance is not None and distance < 5.0:
				self.nearestStationDictionary[block] = closestStation

		return self.nearestStationDictionary

	def station2Blocks(self):
		self.station2Blocks = {}
		for block in self.nearestStationDictionary:
			station = self.nearestStationDictionary[block]
			if station not in self.station2Blocks:
				self.station2Blocks[station] = []
			self.station2Blocks[station].append(block)
		return self.station2Blocks





#B = buildingData()
#B.loadCSV("datasets/PLUTO_Manhattan.csv")