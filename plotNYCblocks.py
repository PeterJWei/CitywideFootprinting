import matplotlib.colorbar as colorbar
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import shapefile as shp
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch
import csv
from pyproj import Proj, transform
import sys
import mpld3
import json
import math
import fiona
#from subwayHistorical import S

#nDictionary = S.loadTurnstile('TurnstileData/turnstile_180811.csv')



class plotNYCblocks:
	def __init__(self, EUI, borough=0):
		self.borough = borough
		self.EUI = EUI
		self.inProj = Proj(init='ESRI:102718', preserve_units=True)
		self.falseProj = Proj(init='ESRI:32054', preserve_units=True)
		self.inProjGoogle = Proj(init='epsg:3857')
		self.outProj = Proj(init='epsg:4326')
		self.PopulationDictionary = {}
		self.PopulationBlock = {}
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
		return

	def exampleRun(self):
		self.instantiateFigure()
		self.drawBoroughs("Boroughs/boroughs.shp")
		self.drawBlocks("BlockLevel/nycb2010.shp")
		self.plotGraph()

		self.instantiateFigure()
		self.drawBoroughs("Boroughs/boroughs.shp")
		print("Drawing Streets...")
		self.drawStreetLines("Centerline/Centerline.shp")
		self.plotGraph()

		self.instantiateFigure()
		self.drawBoroughs("Boroughs/boroughs.shp")
		self.drawSubwayLines("SubwayLines/SubwayLines.shp")
		self.drawSubwayStations("SubwayStations/SubwayStations.shp")
		self.plotGraph()
		return json.dumps(mpld3.fig_to_dict(self.fig))

	def examplePlotRealTime(self, newPopulation):
		self.instantiateFigure()
		self.drawBoroughs("Boroughs/boroughs.shp")
		self.clearPopulation()
		self.dynamicPopulation(newPopulation)
		self.drawBlocks("BlockLevel/nycb2010.shp")
		self.plotGraph()

	def buildingPlot(self):
		self.instantiateFigure()
		self.drawBoroughs("Boroughs/boroughs.shp")
		print("Plotting Buildings")
		self.drawBuildings("buildingLevel/shapefile.shp")
		self.plotGraph()

	def pedestrianCount(self):
		self.instantiateFigure()
		self.drawBoroughs("Boroughs/boroughs.shp")
		self.drawPedestrianCounts()
		self.plotGraph()

	def parkingPlot(self):
		self.instantiateFigure()
		self.drawBoroughs("Boroughs/boroughs.shp")
		self.drawParkingGarages(["ParkingCoordinates/parkingGarageFile.csv",
								"ParkingCoordinates/parkingGarageFile1.csv"])
		self.regularPlot()

	def clearPopulation(self):
		for block in self.PopulationDictionary:
			self.PopulationDictionary[block] = 0

	def dynamicPopulation(self, newPopulation):
		print("Changing Population...")
		print(len(newPopulation))
		total = len(self.PopulationDictionary)
		changed = 0
		for block in newPopulation:
			change = newPopulation[block]
			if block in self.PopulationDictionary:
				self.PopulationDictionary[block] += change
				#if self.PopulationDictionary[block] < 0:
				#	print("Less than 0!")
				#	self.PopulationDictionary[block] = 0
				changed += 1
		print("Total Changed Population: " + str(changed) + "/" + str(total))
		self.MB = self.maxBlock()


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
			if (self.borough == 0 or block[0] == str(self.borough)) and MB < self.PopulationDictionary[block]:
				MB = self.PopulationDictionary[block]
		print("Max Block: " + str(MB))
		return MB

	def minBlock(self):
		MB = 0
		for block in self.PopulationDictionary:
			if (self.borough == 0 or block[0] == str(self.borough)) and MB > self.PopulationDictionary[block]:
				MB = self.PopulationDictionary[block]
		print("Min Block: " + str(MB))
		return MB

	def maxBlockEnergy(self):
		MB = 1
		#for block in self.EUI:
		#	if MB < self.EUI[block]:
		#		MB = self.EUI[block]
		for block in self.PopulationDictionary:
			if (self.borough == 0 or block[0] == str(self.borough)) and self.PopulationDictionary[block] > 0 and block in self.EUI:
				if MB < self.EUI[block]/self.PopulationDictionary[block]:
					MB = self.EUI[block]/self.PopulationDictionary[block]
		print("Max Block: " + str(MB))
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

	def drawParkingGarages(self, parkingGarageFiles):
		points = []
		for file in parkingGarageFiles:
			with open(file, 'rb') as csvfile:
				reader = csv.reader(csvfile, delimiter=',')
				for row in reader:
					points.append((float(row[1]), float(row[2])))
		for i in range(len(points)):
			print(points[i])
			point = points[i]
			R = 1.0
			G = 0.6
			B = 0.6
			newPoints = point
			plt.plot(newPoints[1], newPoints[0], marker='o', markersize = 4, color=(R,G,B))
		return

	def drawPedestrianCounts(self):
		traffic = [3184, 12311, 1235, 8776, 4039, 5940, 2207, 4089, 4193, 4462,
					5968, 4562, 3716, 1572, 5240, 12249, 3732, 3552, 4567, 3355, 2215,
					3992, 8390, 6764, 8512, 2733, 13723, 15513, 16471, 9162, 21634,
					25156, 5560, 7519, 5089, 6516, 28123, 11571, 5371, 10653, 11214,
					4106, 4753, 4356, 3280, 11407, 6685, 5324, 1037]	
		points = [(40.826655,-73.921791),
				(40.862179, -73.895379),
				(40.830343, -73.921037),
				(40.816908, -73.916384),
				(40.855620, -73.867638),
				(40.644282, -74.011191),
				(40.676060, -73.980738),
				(40.667289, -73.981310),
				(40.717581, -73.957973),
				(40.577295, -73.962866),
				(40.650784, -73.948961),
				(40.689388, -73.992571),
				(40.673031, -73.968125),
				(40.650860, -73.958793),
				(40.690882, -73.985871),
				(40.703439, -73.942496),
				(40.692818, -73.987235),
				(40.694597, -73.993433),
				(40.669274, -73.913119),
				(40.587546, -73.954714),
				(40.704616, -74.011551),
				(40.706358, -74.012894),
				(40.771767, -73.981967),
				(40.715985, -74.010148),
				(40.718795, -73.989450),
				(40.735682, -73.992701),
				(40.751741, -73.976758),
				(40.761425, -73.975213),
				(40.710603, -74.008393),
				(40.761275, -73.968957),
				(40.749998, -73.991275),
				(40.707348, -74.010987),
				(40.808286, -73.946872),
				(40.740474, -74.004083),
				(40.849654, -73.934336),
				(40.750468, -73.989218),
				(40.755222, -73.968382),
				(40.757552, -73.973958),
				(40.761805, -73.983905),
				(40.748890, -73.892245),
				(40.748621, -73.884198),
				(40.720383, -73.845341),
				(40.710978, -73.792547),
				(40.703782, -73.796478),
				(40.761208, -73.830909),
				(40.699827, -73.909963),
				(40.637750, -74.075988)]
		self.MB = max(traffic)
		self.MB1 = min(traffic)
		newPoints = (0,0)
		for i in range(len(points)):
			point = points[i]
			t = traffic[i]
			frac = float(t)/float(self.MB)
			R = 1.0
			G = 1.0-frac
			B = 1.0-frac
			newPoints = point
			plt.plot(newPoints[1], newPoints[0], marker='o', markersize = 10, color=(R,G,B))
		return

	def drawBuildings(self,buildingFile):
		sf = shp.Reader(buildingFile)
		fields = sf.fields
		records = sf.records()
		recordlen = len(records)
		i = 0
		for s in sf.shapeRecords():
			i += 1
			R = 1.0
			G = 0.0
			B = 1.0
			if i % 10000 == 0:
				sys.stdout.write("\033[F")
				sys.stdout.write("\033[K")
				print("Drawing shape " + str(i) + " of " + str(recordlen))

			BBL = s.record[9]
			shape = s.shape
			newPoints = []
			for point in shape.points:
				newPoints.append(transform(self.inProj, self.outProj, point[0], point[1]))
			nparts = len(shape.parts)
			if nparts == 1:
				#polygon = Polygon(shape.points)
				polygon = Polygon(newPoints)
				patch = PolygonPatch(polygon, facecolor=[R,G,B], linewidth=0.1, alpha=1.0, zorder=2)
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
					patch = PolygonPatch(polygon, facecolor=[R,G,B], linewidth=0.1, alpha=1.0, zorder=2)
					self.ax.add_patch(patch)

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
		print("\n")
		self.MB = self.maxBlock()
		self.MB1 = self.minBlock()
		if self.MB == 0:
			self.MB = 1.0
		for s in sf.shapeRecords():
			i += 1
			if i % 10000 == 0:
				sys.stdout.write("\033[F")
				sys.stdout.write("\033[K")
				print("Drawing shape " + str(i) + " of " + str(recordlen))
				#print((s.record[3],s.record[4],s.record[5]))
			if s.record[4] not in self.PopulationDictionary: #or s.record[4] not in self.EUI:
				R = 0.0
				G = 0.0
				B = 0.0
				numout += 1
			elif s.record[4] in self.PopulationDictionary and (self.borough != 0 and s.record[4][0] != str(self.borough)):
				R = 0.0
				G = 0.0
				B = 0.0
			elif self.PopulationDictionary[s.record[4]] == 0:
				R = 1.0
				G = 1.0
				B = 1.0
			else:
				pop = self.PopulationDictionary[s.record[4]]
				#energy = self.EUI[s.record[4]]

				#pop = energy/pop

				#print((pop, self.MB))
				if pop > 0:
					frac = float(pop)/float(self.MB)
					#frac = frac/(frac + 0.03) + 0.03/1.03
					R = 1.0
					G = 1.0-frac
					B = 1.0-frac
				elif pop < 0:
					frac = float(pop)/float(self.MB1)
					#frac = frac/(frac + 0.03) + 0.03/1.03
					R = 1.0-frac
					G = 1.0-frac
					B = 1.0
				numin += 1
			shape = s.shape
			newPoints = []
			for point in shape.points:
				newPoints.append(transform(self.inProj, self.outProj, point[0], point[1]))
			nparts = len(shape.parts)
			if nparts == 1:
				#polygon = Polygon(shape.points)
				polygon = Polygon(newPoints)
				patch = PolygonPatch(polygon, facecolor=[R,G,B], linewidth=0.1, alpha=1.0, zorder=2)
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
					patch = PolygonPatch(polygon, facecolor=[R,G,B], linewidth=0.1, alpha=1.0, zorder=2)
					self.ax.add_patch(patch)
		print((numin, numout))

	def drawStreetLines(self, streetsFile):
		sf = shp.Reader(streetsFile)
		fields = sf.fields
		#print(fields)
		records = sf.records()
		recordlen = len(records)
		print("There are " + str(recordlen) + " records")
		j = 0
		for shape in sf.shapeRecords():
			if j == 10000:
				break
			if j % 100 == 0:
				sys.stdout.write("\033[F")
				sys.stdout.write("\033[K")
				print("Drawing shape " + str(j) + " of " + str(recordlen))
			j += 1
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
				plt.plot(x,y,color='blue')
			

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
				plt.plot(x,y,color='blue')

	def drawSubwayStations(self, subwayStationsFile):
		sf = shp.Reader(subwayStationsFile)
		for shape in sf.shapeRecords():
			#print((shape.shape.points[0][0], shape.shape.points[0][1]))
			newPoints = []
			for point in shape.shape.points:
				newPoints.append(transform(self.inProj, self.outProj, point[0], point[1]))
			plt.plot(newPoints[0][0], newPoints[0][1], marker='o', markersize = 3, color='green')

	def regularPlot(self):
		self.ax.autoscale()
		plt.xlabel('Longitude', fontsize=30)
		plt.ylabel('Latitude', fontsize=30)
		plt.xticks(fontsize=20)
		plt.yticks(fontsize=20)
		mng = plt.get_current_fig_manager()
		mng.resize(*mng.window.maxsize())
		plt.show()

	def plotGraph(self):
		axes = {0:[-93.8,-93.38,42.25,42.65],
				1:[-74.034394327,-73.905866485,40.68100549,40.876861617],
				2:None,
				3:None,
				4:None,
				5:None}
		midpoint = 0.5
		popRange = self.MB - self.MB1
		if popRange != 0 and popRange > self.MB:
			midpoint = float(self.MB)/float(self.MB - self.MB1)
		cdic = {'red': ((0.0, 0.0, 0.0),
				(1.0-midpoint, 1.0, 1.0),
				(1.0, 1.0, 1.0)),
		'green': ((0.0, 0.0, 0.0),
				(1.0-midpoint, 1.0, 1.0),
				(1.0, 0.0, 0.0)),
		'blue': ((0.0, 1.0, 1.0),
				(1.0-midpoint, 1.0, 1.0),
				(1.0, 0.0, 0.0))}

		if self.MB1 > 0:
			cdic = {'red': ((0.0, 1.0, 1.0),
				(1.0, 1.0, 1.0)),
			'green': ((0.0, 1.0, 1.0),
				(1.0, 0.0, 0.0)),
			'blue': ((0.0, 1.0, 1.0),
				(1.0, 0.0, 0.0))}
		blueRed1 = LinearSegmentedColormap('BlueRed1', cdic)
		sm = plt.cm.ScalarMappable(cmap=blueRed1, norm = plt.Normalize(vmin=self.MB1, vmax=self.MB))
		sm._A = []
		clb = plt.colorbar(sm)
		clb.ax.tick_params(labelsize=20)
		clb.set_label('Foot Traffic', fontsize=30)

		self.ax.autoscale()
		if axes[self.borough] is not None:
			plt.axis(axes[self.borough])
		#plt.title('Energy Footprint per Capita, Equal Apportionment', fontsize=16)
		plt.xlabel('Longitude', fontsize=30)
		plt.ylabel('Latitude', fontsize=30)
		plt.xticks(fontsize=20)
		plt.yticks(fontsize=20)
		mng = plt.get_current_fig_manager()
		mng.resize(*mng.window.maxsize())
		plt.show()
		#plt.savefig("foo.png")

#P = plotNYCblocks()


