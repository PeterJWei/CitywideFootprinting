import matplotlib.colorbar as colorbar
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import shapefile as shp
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch
import csv
from pyproj import Proj, transform
from subwayHistorical import S

#nDictionary = S.loadTurnstile('TurnstileData/turnstile_180811.csv')



class plotNYCblocks:
	def __init__(self):
		self.inProj = Proj(init='epsg:32054', preserve_units=True)
		self.outProj = Proj(init='epsg:4326')
		self.PopulationDictionary = {}
		self.loadCensusData(1, "CensusData/NYCBlocks/Manhattan.csv")
		print("Loaded Manhattan...")
		self.loadCensusData(2, "CensusData/NYCBlocks/Bronx.csv")
		print("Loaded Bronx...")
		self.loadCensusData(3, "CensusData/NYCBlocks/Kings.csv")
		print("Loaded Kings...")
		self.loadCensusData(4, "CensusData/NYCBlocks/Queens.csv")
		print("Loaded Queens...")
		self.loadCensusData(5, "CensusData/NYCBlocks/Richmond.csv")
		print("Loaded Richmond (Staten Island)...")

		self.MB = self.maxBlock()
		self.instantiateFigure()
		self.drawBoroughs("Boroughs/boroughs.shp")
		self.drawBlocks("BlockLevel/nycb2010.shp")
		self.plotGraph()

		self.instantiateFigure()
		self.drawBoroughs("Boroughs/boroughs.shp")
		self.drawSubwayLines("SubwayLines/SubwayLines.shp")
		self.drawSubwayStations("SubwayStations/SubwayStations.shp")
		self.plotGraph()
		return

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

	def maxBlock(self):
		MB = 0
		for block in self.PopulationDictionary:
			if MB < self.PopulationDictionary[block]:
				MB = self.PopulationDictionary[block]
		return MB

	def instantiateFigure(self):
		self.fig = plt.figure()
		self.ax = plt.axes()
		self.ax.set_aspect('equal')

	def drawBoroughs(self, boroughFile):
		sf = shp.Reader(boroughFile)
		for s in sf.shapeRecords():
			R = 0.5
			G = 0.5
			B = 0.5
			shape = s.shape
			newPoints = []
			for point in shape.points:
				newPoints.append(transform(self.inProj, self.outProj, point[0], point[1]))
				#print(newPoints)
			nparts = len(shape.parts)
			if nparts == 1:
				#polygon = Polygon(shape.points)
				polygon = Polygon(newPoints)
				patch = PolygonPatch(polygon, facecolor=[R,G,B], alpha=1.0, zorder=2)
				self.ax.add_patch(patch)
			else:
				for ip in range(nparts):
					i0 = shape.parts[ip]
					if ip < nparts-1:
						i1 = shape.parts[ip+1]-1
					else:
						i1 = len(shape.points)
					#polygon = Polygon(shape.points[i0:i1+1])
					polygon = Polygon(newPoints[i0:i1+1])
					patch = PolygonPatch(polygon, facecolor=[R,G,B], alpha=1.0, zorder=2)
					self.ax.add_patch(patch)
		# for shape in sf.shapeRecords():
		# 	for i in range(len(shape.shape.parts)):
		# 		i_start = shape.shape.parts[i]
		#         if i==len(shape.shape.parts)-1:
		#             i_end = len(shape.shape.points)
		#         else:
		#             i_end = shape.shape.parts[i+1]
		#         x = [i[0] for i in shape.shape.points[i_start:i_end]]
		#         y = [i[1] for i in shape.shape.points[i_start:i_end]]
		#         plt.plot(x,y)

	def drawBlocks(self, blockFile):
		sf = shp.Reader(blockFile)
		fields = sf.fields
		#print(fields)
		records = sf.records()
		recordlen = len(records)
		print("There are " + str(recordlen) + " records")
		i = 0
		numin = 0
		numout = 0
		for s in sf.shapeRecords():
			i += 1
			if i % 1000 == 0:
				print("Drawing shape " + str(i) + " of " + str(recordlen))
				#print((s.record[3],s.record[4],s.record[5]))
			if s.record[4] not in self.PopulationDictionary:
				R = 0.0
				G = 0.0
				B = 0.0
				numout += 1
			else:
				pop = self.PopulationDictionary[s.record[4]]
				#print((pop, self.MB))
				R = float(pop)/float(self.MB)
				B = 1.0-R
				G = 0.0
				numin += 1
			shape = s.shape
			newPoints = []
			for point in shape.points:
				newPoints.append(transform(self.inProj, self.outProj, point[0], point[1]))
			nparts = len(shape.parts)
			if nparts == 1:
				#polygon = Polygon(shape.points)
				polygon = Polygon(newPoints)
				patch = PolygonPatch(polygon, facecolor=[R,G,B], alpha=1.0, zorder=2)
				self.ax.add_patch(patch)
			else:
				for ip in range(nparts):
					i0 = shape.parts[ip]
					if ip < nparts-1:
						i1 = shape.parts[ip+1]-1
					else:
						i1 = len(shape.points)
					#polygon = Polygon(shape.points[i0:i1+1])
					polygon = Polygon(newPoints[i0:i1+1])
					patch = PolygonPatch(polygon, facecolor=[R,G,B], alpha=1.0, zorder=2)
					self.ax.add_patch(patch)
		print((numin, numout))

	def drawSubwayLines(self, subwayLinesFile):
		sf = shp.Reader(subwayLinesFile)
		for shape in sf.shapeRecords():
			for i in range(len(shape.shape.parts)):
				i_start = shape.shape.parts[i]
				if i==len(shape.shape.parts)-1:
					i_end = len(shape.shape.points)
				else:
					i_end = shape.shape.parts[i+1]
				newPoints = []
				for point in shape.shape.points:
					newPoints.append(transform(self.inProj, self.outProj, point[0], point[1]))
				x = [i[0] for i in newPoints[i_start:i_end]]
				y = [i[1] for i in newPoints[i_start:i_end]]
				plt.plot(x,y,color='red')

	def drawSubwayStations(self, subwayStationsFile):
		sf = shp.Reader(subwayStationsFile)
		for shape in sf.shapeRecords():
			#print((shape.shape.points[0][0], shape.shape.points[0][1]))
			newPoints = []
			for point in shape.shape.points:
				newPoints.append(transform(self.inProj, self.outProj, point[0], point[1]))
			plt.plot(newPoints[0][0], newPoints[0][1], marker='o', markersize = 3, color='green')

	def plotGraph(self):
		self.ax.autoscale()
		plt.show()

P = plotNYCblocks()


