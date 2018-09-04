import csv
import time
from pyproj import Proj, transform
import geopy.distance
import sys
import pickle
import os.path

class buildingData:
	def __init__(self):
		self.boroughCode = {"MN":1,
							"BX":2,
							"BK":3,
							"QN":4,
							"SI":5}
		self.BBL2CT = {}
		self.block2building = {}
		self.inProj = Proj(init='epsg:2263', preserve_units=True)
		self.outProj = Proj(init='epsg:4326')
		self.loadPLUTO("datasets/PLUTO_Manhattan.csv", "Manhattan")
		self.loadPLUTO("datasets/PLUTO_Bronx.csv", "Bronx")
		self.loadPLUTO("datasets/PLUTO_Brooklyn.csv", "Brooklyn")
		self.loadPLUTO("datasets/PLUTO_Queens.csv", "Queens")
		self.loadPLUTO("datasets/PLUTO_Staten.csv", "Staten Island")
		return

	def loadPLUTO(self, PLUTOfile, name):
		print("Loading PLUTO " + name + " File...")
		start = time.time()
		self.loadCSV(PLUTOfile)
		end = time.time()
		print("Finished: " + str(end-start) + " s\n")

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

	def closestStation(self, stationCoordinates, borough=0, name="AllBoroughs"):
		self.nearestStationDictionary = {}
		if os.path.isfile('obj/' + name + '.pkl'):
			print("Pickle Loaded " + name + '.pkl')
			self.nearestStationDictionary = self.load_obj(name)
			#return self.nearestStationDictionary
		else:
			print(name + '.pkl file not found.\n')
			totalBlocks = len(self.block2building)
			blockNo = 0
			for block in self.block2building:
				blockNo += 1
				if blockNo % (totalBlocks/100) == 0:
					sys.stdout.write("\033[F")
					sys.stdout.write("\033[K")
					print(str(int(round(float(blockNo)/float(totalBlocks)*100))) + "%...")
				if borough != 0 and block[0] != str(borough):
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
			self.save_obj(self.nearestStationDictionary, name)
			print("Pickle Saved " + name + '.pkl')
		return self.nearestStationDictionary

	def station2Blocks(self):
		self.station2Blocks = {}
		for block in self.nearestStationDictionary:
			station = self.nearestStationDictionary[block]
			if station not in self.station2Blocks:
				self.station2Blocks[station] = []
			self.station2Blocks[station].append(block)
		return self.station2Blocks

	def save_obj(self, obj, name):
		with open('obj/'+ name + '.pkl', 'wb') as f:
			pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

	def load_obj(self, name):
		with open('obj/' + name + '.pkl', 'rb') as f:
			return pickle.load(f)



#B = buildingData()
#B.loadCSV("datasets/PLUTO_Manhattan.csv")