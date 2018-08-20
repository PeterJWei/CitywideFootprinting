from Remote2StopID import remoteDictionary
from buildingData import buildingData
from plotNYCblocks import plotNYCblocks

S = remoteDictionary()
B = buildingData()

nearestStation = B.closestStation(S.coordinates)
new = B.station2Blocks()
timeSeriesEntries = S.timeSeriesDataEntries
timeSeriesExits = S.timeSeriesDataExits
#for block in B.block2building:
	#print(B.block2building[block])
#	(lat,lon) = B.block2building[block][0]
#	for station in S.coordinates:		


P = plotNYCblocks()