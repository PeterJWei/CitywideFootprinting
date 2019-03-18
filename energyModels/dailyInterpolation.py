import csv
from datetime import datetime


class interpolation:
	def __init__(self):
		# self.fileNames = ['FullServiceRestaurant', 'Hospital', 'LargeHotel', 'LargeOffice', 'MediumOffice', 
		# 	'MidriseApartment', 'OutPatient', 'PrimarySchool', 'QuickServiceRestaurant', 'SecondarySchool',
		# 	'SmallHotel', 'Stand-aloneRetail', 'StripMall', 'SuperMarket', 'Warehouse']
		self.fileNames = ['MidriseApartment', 'LargeOffice', 'Stand-aloneRetail', 'Warehouse']
		self.footprints = {}
		self.totals = {}
		self.instantiateFootprints()
		self.loadEnergy()
		self.stats()

	def stats(self):
		for buildType in self.footprints:
			footprint = self.footprints[buildType]
			totalEnergy = [0.0]*12
			for i, power in enumerate(footprint):
				totalEnergy[i/730] += power
			self.totals[buildType] = totalEnergy
			
	def loadEnergy(self):
		for f in self.fileNames:
			with open ('NewYorkReference/' + f + '.csv', 'rb') as csvfile:
				reader = csv.reader(csvfile, delimiter=',')
				header = True
				i = 0
				for row in reader:
					if header:
						header = False
						continue
					if len(row[0]) != 16:
						print("Not equal")
					year = 2005
					month = int(row[0][1:3])
					day = int(row[0][4:6])
					hour = int(row[0][8:10])
					minute = int(row[0][11:13])
					second = int(row[0][14:])
					if hour == 24:
						hour = 0
						if month == 12 and day == 31:
							year = 2006
							month = 1
							day = 1
						elif month in [1, 3, 5, 7, 8, 10] and day == 31:
							day = 1
							month = month + 1
						elif month == 2 and day == 28:
							day = 1
							month = 3
						elif month in [4, 6, 9, 11] and day == 30:
							day = 1
							month = month + 1
						else:
							day = day + 1
					dt = datetime(year, month, day, hour)
					start = datetime(2005, 1, 1, 1)
					electric = float(row[1])
					hoursSince = int((dt - start).total_seconds()/3600)
					i += 1
					self.footprints[f][hoursSince] = electric
				#print(i)
			# fans = float(row[2])
			# cooling = float(row[3])
			# heating = float(row[4])
			# lights = float(row[5])
			# equipment = float(row[6])

	def instantiateFootprints(self):
		for name in self.fileNames:
			self.footprints[name] = [0] * 8760

I = interpolation()