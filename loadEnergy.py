import csv

class loadEnergy:
	def __init__(self):
		self.loadLL84("LL84NYCBuildings.csv")
		return

	def loadLL84(self, LL84File):
		with open(blockFile, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = True
			for row in reader:
				if i: #skip the first line
					i = False
					continue
				else:
					BBL = row[5]
					EUI = row[43]