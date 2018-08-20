from Remote2StopID import remoteDictionary
from buildingData import buildingData
from plotNYCblocks import plotNYCblocks

S = remoteDictionary()
B = buildingData()

for block in B.block2building:
	#print(B.block2building[block])
	(lat,lon) = B.block2building[block][0]
	for station in S.coordinates:
		


P = plotNYCblocks()