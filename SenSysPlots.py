from plotNYCblocks import plotNYCblocks
from datetime import datetime, timedelta
from dynamicPopulation import showDynamicPopulation
import matplotlib.pyplot as plt
import DBMgr
from dateutil.parser import *
import csv
#NYC Voronoi Diagram
if False:
	P = plotNYCblocks({},0)
	P.sensysPlots()

#NYC turnstiles
if False:
	DP = showDynamicPopulation()
	plt.figure()
	for station in DP.timeSeriesEntries:
		entries = DP.timeSeriesEntries[station]
		exits = DP.timeSeriesExits[station]
		newEntries = []
		newExits = []
		for i in range(len(entries)-1):
			newEntries.append(entries[i+1] - entries[i])
			newExits.append(exits[i+1] - exits[i])
		
		t = [datetime(2019, 4, 7, 0, 0, 0) + timedelta(hours=x*4) for x in range(len(entries)-1)]
		plt.plot(t, newEntries, t, newExits, linewidth=4)

		#plt.plot(t, Y, linewidth=4)
		plt.xlabel("Time", fontsize=16)
		plt.ylabel("Turnstile Counts", fontsize=16)
		plt.gcf().autofmt_xdate()
		plt.legend(["Entries", "Exits"])
		plt.show()
		break

#Energy Consumption Plots
if False:
	Residential1 = [54707, 54713, 54721, 54725, 54737, 54743, 54748, 54753, 54757, 54762, 54769, 54773, 54777, 54782, 54799]
	d = [datetime(2019, 3, 11, 19), datetime(2019, 3, 13, 12), datetime(2019, 3, 15, 12), datetime(2019, 3, 16, 11), datetime(2019, 3, 19, 9), datetime(2019, 3, 20, 9), datetime(2019, 3, 22, 8), datetime(2019, 3, 23, 12), datetime(2019, 3, 24, 12), datetime(2019, 3, 25, 10), datetime(2019, 3, 27, 11), datetime(2019, 3, 28, 10), datetime(2019, 3, 29, 12),datetime(2019, 3, 30, 12),datetime(2019, 4, 3, 12)]
	plt.plot(d, Residential1, linewidth=4)
	plt.xlabel("Time", fontsize=16)
	plt.ylabel("Energy Consumption (kWh)", fontsize=16)
	plt.show()

if True:
	db = DBMgr.DBMgr()
	footprint = db.getEnergyFootprint("45458C82-9CE4-412F-8BD7-0D45CA175508")
	timestamps = []
	powers = []
	with open("footprint.csv", 'wb') as csvfile:
		for (t,power) in footprint:
			csvwriter.writerow([t, power])

