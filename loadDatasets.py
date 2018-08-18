# >>> import csv
# >>> with open('eggs.csv', 'rb') as csvfile:
# ...     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
# ...     for row in spamreader:
# ...         print ', '.join(row)

###### Formatted Data
data = {}
data["bbl"] = [] #71
data["buildClass"] = [] #28
data["landUse"] = [] #29
data["lotArea"] = [] #33
data["buildingArea"] = [] #34
data["commercialArea"] = [] #35
data["residentialArea"] = [] #36
data["officeArea"] = [] #37
data["retailArea"] = [] #38
data["garageArea"] = [] #39
data["storageArea"] = [] #40
data["factoryArea"] = [] #41
data["otherArea"] = [] #42
data["buildCount"] = [] #44
data["floorCount"] = [] #45
data["residentialUnits"] = [] #46
data["totalUnits"] = [] #47
data["buildingFrontage"] = [] #50
data["buildingDepth"] = [] #51
data["yearBuilt"] = [] #61
data["xCoord"] = [] #74
data["yCoord"] = [] #75

def printLoading(index, total, intervals):
	if (index + 1) % (total/intervals) == 0:
		print(str(round(float(index+1)/float(total) * 100)) + "%")

import csv
with open('datasets/PLUTO_Manhattan.csv', 'rb') as csvfile:
	dataReader = csv.reader(csvfile, delimiter=',')
	data1 = list(dataReader)
	#print(len(data1))
	labels = True
	x = len(data1)
	for index,row in enumerate(data1):
		printLoading(index, x, 10)
		if labels:
			for i in range(len(row)):
				#print(str(i) + "," + row[i])
				break
			labels = False
		else:
			data["bbl"].append(row[71])
			data["buildClass"].append(row[28])
			data["landUse"].append(row[29])
			data["lotArea"].append(row[33])
			data["buildingArea"].append(row[34])
			data["commercialArea"].append(row[35])
			data["residentialArea"].append(row[36])
			data["officeArea"].append(row[37])
			data["retailArea"].append(row[38])
			data["garageArea"].append(row[39])
			data["storageArea"].append(row[40])
			data["factoryArea"].append(row[41])
			data["otherArea"].append(row[42])
			data["buildCount"].append(row[44])
			data["floorCount"].append(row[45])
			data["residentialUnits"].append(row[46])
			data["totalUnits"].append(row[47])
			data["buildingFrontage"].append(row[50])
			data["buildingDepth"].append(row[51])
			data["yearBuilt"].append(row[61])
			data["xCoord"].append(row[74])
			data["yCoord"].append(row[75])

