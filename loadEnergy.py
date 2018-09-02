import csv

class loadEnergy:
	def __init__(self):
		self.energyDictionary = {}
		self.loadLL84("LL84NYCBuildings.csv")
		return

	def loadLL84(self, LL84File):
		with open(LL84File, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = True
			for row in reader:
				if i: #skip the first line
					i = False
					continue
				else:
					BBL = row[5]
					BBLs = BBL.split(";")

					EUI = row[43]
					try:
						EUI = float(EUI)
					except ValueError:
						EUI = 0.0
					for b in BBLs:
						self.energyDictionary[b] = EUI/365.0/24.0
