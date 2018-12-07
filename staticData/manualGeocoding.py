import csv
from googlegeocoder import GoogleGeocoder
from pyproj import Proj, transform
import geopy.distance
import sys
import math

class reverseGeocode:
	def __init__(self):
		self.inProj = Proj(init='epsg:2263', preserve_units=True)
		self.outProj = Proj(init='epsg:4326')
		self.buildingCoordinates = {}
		self.geocoding = []

	def parseBuildingCSV(self, file):
		print("Parsing Building CSV...")
		with open (file, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = True
			j = 0
			for row in reader:
				j += 1
				if i:
					i = False
					continue
				else:
					if j % 1000 == 0:
						sys.stdout.write("\033[F")
						sys.stdout.write("\033[K")
						print("Saving coordinates for point " + str(j) + " of " + str(42967))
					borough = row[0]
					block = row[1]
					lot = row[2]
					# if len(block) < 5:
					# 	block = "0" * (5-len(block)) + block
					# if len(lot) < 4:
					# 	lot = "0" * (4-len(lot)) + lot
					# BBL = B + block + lot
					xcoord = row[74]
					ycoord = row[75]
					if len(xcoord) == 0 or len(ycoord) == 0:
						continue
					lon, lat = transform(self.inProj, self.outProj, float(xcoord), float(ycoord))
					self.buildingCoordinates[(lon, lat)] = (borough, block, lot)
		print("Checkpoint 1: " + str(len(self.buildingCoordinates)))

	def parseDataCSV(self, file):
		print("Parsing CSV Data...")
		with open (file, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = True
			j = 0
			for row in reader:
				j += 1
				if i:
					i = False
					continue
				else:
					if j % 10 == 0:
						sys.stdout.write("\033[F")
						sys.stdout.write("\033[K")
						print("Searching for point " + str(j) + " of " + str(227429))
					dataLat = float(row[0])
					dataLon = float(row[1])
					hour = row[2]
					minute = row[3]
					m = .05
					bestBBL = None
					for coord in self.buildingCoordinates:
						(lon, lat) = coord
						dist = math.sqrt((lon - dataLon)**2 + (lat - dataLat)**2)
						if m > dist:
							m = dist
							bestBBL = self.buildingCoordinates[coord]
					if bestBBL is not None:
						self.geocoding.append((bestBBL[0], bestBBL[1], bestBBL[2], hour, minute))
		print("Checkpoint 2: " + str(len(self.geocoding)) + " data written")

	def saveCSV(self, fileName):
		print("Saving Data...")
		with open(fileName, 'wb') as csvfile:
			i = 0
			csvwriter = csv.writer(csvfile, delimiter=',')
			csvwriter.writerow(["Borough", "Block", "Lot", "Hour", "Minute"])
			for datum in self.geocoding:
				csvwriter.writerow([datum[0], datum[1], datum[2], datum[3], datum[4]])
				i += 1


R = reverseGeocode()
R.parseBuildingCSV("../datasets/PLUTO_Manhattan.csv")
R.parseDataCSV("../static/endLocations.csv")
R.saveCSV("TaxiDestinationBBL.csv")


