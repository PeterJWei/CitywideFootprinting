from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import csv
from collections import OrderedDict

(x0, y0, x1, y1) = (40.6, -74.03, 40.9, -73.9)
cx = (x0+x1)/2
cy = (y0+y1)/2
fig, ax = plt.subplots()
m = Basemap(projection='merc',area_thresh=0.1,llcrnrlat=x0,urcrnrlat=x1,
            llcrnrlon=y0,urcrnrlon=y1,lat_0=cx,lon_0=cy,resolution='f')
 
m.drawcoastlines()
m.drawcountries()
m.drawrivers()
#m.fillcontinents(color = 'coral')
m.drawmapboundary()

m.readshapefile('nynta_18b/nyntaWGS84', 'nyntaWGS84')

print("Done loading map.")

propertyDictionary = {}
propertyDictionary2 = {}
with open ('EnergyDataset1.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	#print("Number of datapoints: " + str(len(list(reader))))
	for row in reader:
		propType = row[15]
		if propType not in propertyDictionary:
			rColor = np.random.uniform(0.7, 1.0, 3)
			colorTuple = (rColor[0], rColor[1], rColor[2])
			propertyDictionary[propType] = colorTuple
			propertyDictionary2[propType] = 1
		else:
			propertyDictionary2[propType] += 1

for prop in propertyDictionary2:
	print(prop + " :" + str(propertyDictionary2[prop]))

with open ('EnergyDataset1.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	#print("Number of datapoints: " + str(len(list(reader))))
	for row in reader:
		propType = row[15]
		lat = row[54]
		try:
			lat = float(lat)
		except ValueError:
			continue
		lon = row[55]
		try:
			lon = float(lon)
		except ValueError:
			continue
		#print((lat,lon))
		x,y = m(lon, lat)
		m.plot(x, y, 'o', color=propertyDictionary[propType], label=propType, markersize=2)

handles, labels = plt.gca().get_legend_handles_labels()
by_label = OrderedDict(zip(labels, handles))
leg = plt.legend(by_label.values(), by_label.keys(), markerscale=5, loc='center left')
plt.draw()

bb = leg.get_bbox_to_anchor().inverse_transformed(ax.transAxes)
xOffset = 1.5
bb.x0 += xOffset
bb.x1 += xOffset
leg.set_bbox_to_anchor(bb, transform=ax.transAxes)
plt.show()