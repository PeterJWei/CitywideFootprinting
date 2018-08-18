import csv
from pyproj import Proj, transform


class buildingData:
	def __init__(self):
		self.boroughCode = {"MN":1}
		self.inProj = Proj(init='epsg:2263', preserve_units=True)
		self.outProj = Proj(init='epsg:4326')

		return

	def loadCSV(self, PLUTOfile):
		self.block2building = {}
		with open (PLUTOfile, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = True
			for row in reader: 
				if i: #skip the first line
					i = False
					continue
				else:
					borough = row[0]
					CT2010 = row[4]
					CB2010 = row[5]
					block = self.boroughCode[borough] + CT2010 + CB2010
					if len(CT2010) == 0 or len(CB2010) == 0 or borough not in self.boroughCode:
						continue
					xcoord = row[74]
					ycoord = row[75]
					if len(xcoord) == 0 or len(ycoord) == 0:
						continue
					latlon = transform(self.inProj, self.outProj, xcoord, ycoord)

					#match latlon to nearest subway

					if block not in self.block2building:
						self.block2building[block] = []
					self.block2building[block].append(latlon)








B = buildingData()
B.loadCSV("datasets/PLUTO_Manhattan.csv")