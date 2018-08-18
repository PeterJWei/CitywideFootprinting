import matplotlib.colorbar as colorbar
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import shapefile as shp
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch
import csv
from subwayHistorical import S

nDictionary = S.loadTurnstile('TurnstileData/turnstile_180811.csv')

CensusDictionary = {}

with open ('CensusData/nyc2010Census2NTA.csv', 'rb') as csvfile:
	data = [row for row in csv.reader(csvfile.read().splitlines())]
	reader = data
	#reader = csv.reader(csvfile, delimiter=',')
	i = 0
	for row in reader: 
		i += 1
		if i <= 5: #skip the first 5 lines
			continue
		else:
			CT = row[3] #census tract
			NTA = row[5] #Neighborhood Tabulation Area
			CensusDictionary[CT] = NTA

print(CensusDictionary)

def readBlockGroups(blockGroups):
	PopulationDictionary = {}
	with open (blockGroups, 'rb') as csvfile:
		#data = [row for row in csv.reader(csvfile.read().splitlines())]
		#reader = data
		reader = csv.reader(csvfile, delimiter=',')
		i = 0
		for row in reader: 
			i += 1
			#print(row)
			if i <= 2: #skip the first 2 lines
				continue
			else:
				GEOid2 = row[1]
				CT = GEOid2[5:-1] #convert GEOid2 to census tract (bits 5-12)
				estimated = row[3] #estimated populations
				NTA = ""
				if CT not in CensusDictionary:
					print(CT)
					continue
				else:
					NTA = CensusDictionary[CT] #get the NTA
				if NTA not in PopulationDictionary:
					PopulationDictionary[NTA] = 0
				PopulationDictionary[NTA] += int(estimated) #add census tract count to NTA
	return PopulationDictionary

PDNewYork = readBlockGroups('CensusData/NewYorkBlockGroups/NewYorkBlockGroups.csv')
PDBronx = readBlockGroups('CensusData/BronxBlockGroups/BronxBlockGroups.csv')
PDKings = readBlockGroups('CensusData/KingsBlockGroups/KingsBlockGroups.csv')
PDQueens = readBlockGroups('CensusData/QueensBlockGroups/QueensBlockGroups.csv')
PDRichmond = readBlockGroups('CensusData/RichmondBlockGroups/RichmondBlockGroups.csv')


########################## Get Union of the dictionaries #####################
NewYorkSet = set(PDNewYork.keys())
PDBronxSet = set(PDBronx.keys())
PDKingsSet = set(PDKings.keys())
PDQueensSet = set(PDQueens.keys())
PDRichmondSet = set(PDRichmond.keys())

TotalSet = NewYorkSet | PDBronxSet | PDKingsSet | PDQueensSet | PDRichmondSet
TotalDictionary = dict.fromkeys(list(TotalSet), 0)

for key in PDNewYork:
	if TotalDictionary[key] < PDNewYork[key]:
		TotalDictionary[key] = PDNewYork[key]
for key in PDBronx:
	if TotalDictionary[key] < PDBronx[key]:
		TotalDictionary[key] = PDBronx[key]
for key in PDKings:
	if TotalDictionary[key] < PDKings[key]:
		TotalDictionary[key] = PDKings[key]
for key in PDQueens:
	if TotalDictionary[key] < PDQueens[key]:
		TotalDictionary[key] = PDQueens[key]
for key in PDRichmond:
	if TotalDictionary[key] < PDRichmond[key]:
		TotalDictionary[key] = PDRichmond[key]
##############################################################################



maxNTA = 0
for nta in TotalDictionary:
	if TotalDictionary[nta] > maxNTA:
		maxNTA = TotalDictionary[nta]
print(maxNTA)

fig = plt.figure()
ax = plt.axes()
ax.set_aspect('equal')
icolor = 1
sf = shp.Reader("Boroughs/boroughs.shp")
for shape in sf.shapeRecords():
	for i in range(len(shape.shape.parts)):
		i_start = shape.shape.parts[i]
        if i==len(shape.shape.parts)-1:
            i_end = len(shape.shape.points)
        else:
            i_end = shape.shape.parts[i+1]
        x = [i[0] for i in shape.shape.points[i_start:i_end]]
        y = [i[1] for i in shape.shape.points[i_start:i_end]]
        plt.plot(x,y)

sf = shp.Reader("nynta_18b/nynta.shp")
#sf = shp.Reader("BlockLevel/shapefile.shp")
fields = sf.fields
print(fields)
for s in sf.shapeRecords():
	#print(s.record[0:4]) 0- Borough Code, 1- Borough Name, 2- County FIPS, 3- NTA Code, 4- NTA Name
	if s.record[3] not in TotalDictionary:
		print(s.record[3])
		R = 0.0
		G = 0.0
		B = 0.0
	else:
		pop = TotalDictionary[s.record[3]]
		if s.record[3] in nDictionary:
			pop += nDictionary[s.record[3]][3]
			print(nDictionary[s.record[3]][3])
		R = float(pop)/float(maxNTA)
		G = 0.0
		B = 1.0-R
	shape = s.shape
	nparts = len(shape.parts) # total parts
	if nparts == 1:
		polygon = Polygon(shape.points)
		patch = PolygonPatch(polygon, facecolor=[R,G,B], alpha=1.0, zorder=2)
		ax.add_patch(patch)
	else:
		for ip in range(nparts):
			i0 = shape.parts[ip]
			if ip < nparts-1:
				i1 = shape.parts[ip+1]-1
			else:
				i1 = len(shape.points)
			polygon = Polygon(shape.points[i0:i1+1])
			patch = PolygonPatch(polygon, facecolor=[R,G,B], alpha=1.0, zorder=2)
			ax.add_patch(patch)
			#plt.text(shape.points[i0][0], shape.points[i0][1], s.record[3], horizontalalignment='center')


#	for i in range(len(shape.shape.parts)):
#		i_start = shape.shape.parts[i]
#		if i==len(shape.shape.parts)-1:
#			i_end = len(shape.shape.points)
#		else:
#			i_end = shape.shape.parts[i+1]
#		x = [i[0] for i in shape.shape.points[i_start:i_end]]
#		y = [i[1] for i in shape.shape.points[i_start:i_end]]
#		plt.plot(x,y)

cdic = {'red': ((0.0, 0.0, 0.0),
				(1.0, 1.0, 1.0)),
		'green': ((0.0, 0.0, 0.0),
				(1.0, 0.0, 0.0)),
		'blue': ((0.0, 1.0, 1.0),
				(1.0, 0.0, 0.0))}
blueRed1 = LinearSegmentedColormap('BlueRed1', cdic)
sm = plt.cm.ScalarMappable(cmap=blueRed1, norm = plt.Normalize(vmin=0, vmax=maxNTA))
sm._A = []
clb = plt.colorbar(sm)
clb.set_label('Population of Block Group')
plt.title('Population of New York City, Nighttime', fontsize=16)
plt.show()
