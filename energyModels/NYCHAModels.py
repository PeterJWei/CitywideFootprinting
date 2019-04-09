import csv
import time
import numpy as np
import pandas as pd
import math
from datetime import datetime, timedelta
from generateWeather import weather
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import pickle


class NYCHAAnalysis:
	def __init__(self):
		self.boroughCode = {"MN":1,"BX":2,"BK":3,"QN":4,"SI":5}
		self.bbl2pluto = {}
		self.loadPLUTO("../datasets/PLUTO_Manhattan.csv")
		self.loadPLUTO("../datasets/PLUTO_Brooklyn.csv")
		self.loadPLUTO("../datasets/PLUTO_Bronx.csv")
		self.loadPLUTO("../datasets/PLUTO_Queens.csv")
		self.loadPLUTO("../datasets/PLUTO_Staten.csv")
		self.file = "NYCHA.csv"
		self.propertyFile = "PropertyDirectory.csv"
		self.baseData = None
		self.OLSData = None
		self.target = None
		self.bin2bbl = {}
		self.bbl2bin = {}
		self.building2bin = {}
		W = weather('weatherData.csv')
		self.weatherList = W.weatherList
		#self.viewHeader(self.file)
		#self.loadProperty(self.propertyFile)
		self.loadData()
		self.loadbin2bbl("bobaadr.txt")
		self.loadbuilding2bin("development.csv")
		#self.buildingKeys()
		#self.binKeys()
		self.convert()
		self.OLS()
		#self.transferData()
		#self.OLS()
		#self.statistics()

	def OLS(self):
		self.baseData = self.baseData[['Manhattan', 'Brooklyn', 'Queens', 'Bronx',
					'Staten', 'DPmax', 'DPmin', 'DPavg', 'DBmax', 'DBmin', 'DBavg',
					'totalArea', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'commercial', 'residential', 'office',
					'retail', 'garage', 'storage', 'factory', 'other']]
		# self.baseData = self.baseData[['Manhattan', 'Brooklyn', 'Queens', 'Bronx',
		# 			'Staten', 'DBmax', 'DBmin', 'DBavg',
		# 			'totalArea', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'residential', 'office',
		# 			'retail', 'garage', 'storage', 'factory']]
		# self.baseData = self.baseData[['Manhattan', 'Brooklyn', 'Queens', 'Bronx',
		# 			'Staten', 'DPmax', 'DPmin', 'DPavg', 'DBmax', 'DBmin', 'DBavg',
		# 			'totalArea', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'residential', 'office',
		# 			'retail', 'storage', 'factory']]
		print(self.baseData.columns)
		X_train, X_test, y_train, y_test = train_test_split(self.baseData, self.target, test_size=0.33, random_state=42)
		#X = self.OLSData
		#y = self.target
		lm = linear_model.LinearRegression()
		model = lm.fit(X_train,y_train)
		filename = 'NYCHARegressionModel.sav'
		pickle.dump(model, open(filename, 'wb'))
		#score = lm.score(X,y)
		predictions = lm.predict(X_test)
		print("Total samples: " + str(len(self.baseData)))
		print("Number of test samples: " + str(len(y_test)))
		print("Mean Absolute Error: %.2f" % mean_absolute_error(y_test, predictions))
		print("Mean Squared Error: %.2f" % mean_squared_error(y_test, predictions))
		print("Variance Score: %.2f" % r2_score(y_test, predictions))


	def viewHeader(self, filename):
		with open(filename, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for row in reader:
				i = 0
				for column in row:
					#print(str(i) + " :" + column)
					i += 1
				break

	def loadPLUTO(self, file):
		print("Loading " + file + "...")
		start = time.time()
		self.loadCSV(file)
		end = time.time()
		print("Finished: " + str(end-start) + " s\n")

	def loadCSV(self, PLUTOfile):
		with open (PLUTOfile, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = True
			for row in reader:
				if i: #skip the first line
					#for j in range(len(row)):
					#	print((j, row[j]))
					i = False
					continue
				else:
					borough = row[0]
					block = row[1]
					lot = row[2]
					B = str(self.boroughCode[borough])
					if len(block) < 5:
						block = "0" * (5-len(block)) + block
					if len(lot) < 4:
						lot = "0" * (4-len(lot)) + lot
					BBL = B + block + lot
					GFA = float(row[34])
					areaCom = float(row[35])
					areaRes = float(row[36])
					areaOff = float(row[37])
					areaRet = float(row[38])
					areaGar = float(row[39])
					areaSto = float(row[40])
					areaFac = float(row[41])
					areaOth = float(row[42])
					yearBuilt = int(row[61])

					self.bbl2pluto[BBL] = (GFA, yearBuilt, areaCom, areaRes, areaOff, areaRet, areaGar, areaSto, areaFac, areaOth)

	def loadData(self):
		Development = []
		Borough = []
		# ServiceStart = []
		# ServiceEnd = []
		DPhigh = []
		DPlow = []
		DPmean = []
		DBhigh = []
		DBlow = []
		DBmean = []
		Consumption = []
		Charges = []
		Buildings = []
		Manhattan = []
		Brooklyn = []
		Queens = []
		Bronx = []
		StatenIsland = []
		boroughDictionary = {'':0, 'MANHATTAN':1, 'BROOKLYN':2, 'QUEENS':3, 'BRONX':4, 'STATEN ISLAND':5}
		with open(self.file, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = True
			for row in reader:
				if i:
					i = not i
					continue
				Building = 0
				index = row[3].find('BLD')
				#print(row[3][index:])
				if index >= 0 and index < len(row[3])-6:
					try:
						Building = int(row[3][index+4:index+6])# if index != len(row[3])-6 else int(row[3][index+4:])
					except ValueError:
						continue
				else: continue
				if Building == 0:
					continue

				f = "%m/%d/%Y"
				st = datetime.strptime(row[14], f).date()
				et = datetime.strptime(row[15], f).date()
				delta = et - st

				DPmax = None
				DPmin = None
				DPtotal = 0
				DBmax = None
				DBmin = None
				DBtotal = 0
				samples = 0
				#print("Testing dictionary...")
				for i in range(delta.days + 1):
					newDate = st + timedelta(i)
					if (newDate.year, newDate.month, newDate.day) not in self.weatherList:
						continue
					(DP1, DP2, DP3, DB1, DB2, DB3, s) = self.weatherList[(newDate.year, newDate.month, newDate.day)]
					DPmax = DP1 if (DPmax is None or DPmax < DP1) else DPmax
					DPmin = DP2 if (DPmin is None or DPmin > DP2) else DPmin
					DPtotal += DP3
					DBmax = DB1 if (DBmax is None or DBmax < DB1) else DBmax
					DBmin = DB2 if (DBmin is None or DBmin > DB2) else DBmin
					DBtotal += DB3
					samples += s
				if DPmax is None:
					continue

				cons = 0
				try:
					cons = math.log(float(row[22]))
				except:
					if abs(float(row[22])) < 0.0001:
						continue
					else:
						print(row[22])
						continue

				Consumption.append(cons)
				DPavg = DPtotal*1.0/DP3
				DBavg = DBtotal*1.0/DB3
				DPhigh.append(DPmax)
				DPlow.append(DPmin)
				DPmean.append(DPavg)
				DBhigh.append(DBmax)
				DBlow.append(DBmin)
				DBmean.append(DBavg)
				# ServiceStart.append(row[14])
				# ServiceEnd.append(row[15])

				#print("Building Number: " + str(Building))
				Buildings.append(Building)
				Dev = row[0]
				if Dev == '1162-1176 WASHINGTON AVENUE':
					Dev = 'WASHINGTON AVENUE'
				Development.append(Dev)

				Borough.append(row[1])
				b = [0, 0, 0, 0, 0, 0]
				b[boroughDictionary[row[1]]] = 1
				Manhattan.append(b[1])
				Brooklyn.append(b[2])
				Queens.append(b[3])
				Bronx.append(b[4])
				StatenIsland.append(b[5])
				f = "%m/%d/%Y"#"%Y-%m-%dT%H:%M:%S"

				Charges.append(row[23])

		self.OLSData = pd.DataFrame({
			'Development': Development,
			'Building': Buildings,
			'Manhattan': Manhattan,
			'Brooklyn': Brooklyn,
			'Queens': Queens,
			'Bronx': Bronx,
			'Staten': StatenIsland,
			# 'Start': ServiceStart,
			# 'End': ServiceEnd,
			'DPmax': DPhigh,
			'DPmin': DPlow,
			'DPavg': DPmean,
			'DBmax': DBhigh,
			'DBmin': DBlow,
			'DBavg': DBmean,
			'Consumption': Consumption,
			#'Charges': Charges
			})
		self.OLSData = self.OLSData.drop(self.OLSData[(self.OLSData['Development'] == 'BAYCHESTER') & (self.OLSData['Building'] == 12)].index)
		self.OLSData = self.OLSData.drop(self.OLSData[(self.OLSData['Development'] == 'HOPE GARDENS') & (self.OLSData['Building'] == 6)].index)
		self.OLSData = self.OLSData.drop(self.OLSData[(self.OLSData['Development'] == 'FOREST HILLS COOP (108TH STREET-62ND DRIVE)') & (self.OLSData['Building'] == 4)].index)

	def buildingKeys(self):
		for key in sorted(self.building2bin.keys(), key=lambda x:x[0]):
			print(key)

	def binKeys(self):
		for key in sorted(self.bin2bbl.keys()):
			print(key)

	def convert(self):
		bins = []
		bbl = []
		totalArea = []
		built = []
		commercial = []
		residential = []
		office = []
		retail = []
		garage = []
		storage = []
		factory = []
		other = []
		Years1 = []
		Years2 = []
		Years3 = []
		Years4 = []
		Years5 = []
		for row in self.OLSData[['Development','Building']].itertuples(index=True, name='Pandas'):
			try:
				BIN = self.building2bin[(row.Development, row.Building)]
				bins.append(BIN)
			except KeyError:
				print((row.Development, row.Building))
		for BIN in bins:
			try:
				BBL = self.bin2bbl[BIN]
				floorArea = 0.0
				YB = 0.0
				aCom = 0.0
				aRes = 0.0
				aOff = 0.0
				aRet = 0.0
				aGar = 0.0
				aSto = 0.0
				aFac = 0.0
				aOth = 0.0
				for lot in BBL:
					(GFA, yearBuilt, areaCom, areaRes, areaOff, 
						areaRet, areaGar, areaSto, areaFac, areaOth) = self.bbl2pluto[lot]
					floorArea += float(GFA)
					YB += int(yearBuilt)
					aCom += float(areaCom)
					aRes += float(areaRes)
					aOff += float(areaOff)
					aRet += float(areaRet)
					aGar += float(areaGar)
					aSto += float(areaSto)
					aFac += float(areaFac)
					aOth += float(areaOth)
				YB = YB / len(BBL)
				YBarr = [0, 0, 0, 0, 0]
				if YB <= 1930:
					YBarr[0] = 1
				elif YB > 1930 and YB <= 1950:
					YBarr[1] = 1
				elif YB > 1950 and YB <= 1970:
					YBarr[2] = 1
				elif YB > 1970 and YB <= 1990:
					YBarr[3] = 1
				elif YB > 1990:
					YBarr[4] = 1
				Years1.append(YBarr[0])
				Years2.append(YBarr[1])
				Years3.append(YBarr[2])
				Years4.append(YBarr[3])
				Years5.append(YBarr[4])
				totalArea.append(math.log(floorArea))
				built.append(YB)
				commercial.append(aCom/floorArea)
				residential.append(aRes/floorArea)
				office.append(aOff/floorArea)
				retail.append(aRet/floorArea)
				garage.append(aGar/floorArea)
				storage.append(aSto/floorArea)
				factory.append(aFac/floorArea)
				other.append(aOth/floorArea)
			except KeyError:
				print(str(BIN))
				#continue
		#self.baseData['BIN'] = pd.Series(bins, index=self.baseData.index)
		#Split to parameters and target
		self.baseData = self.OLSData[['Manhattan', 'Brooklyn', 'Queens', 'Bronx',
					'Staten', 'DPmax', 'DPmin', 'DPavg', 'DBmax', 'DBmin', 'DBavg']]
		self.target = self.OLSData[['Consumption']]

		self.baseData['totalArea'] = pd.Series(totalArea, index=self.baseData.index)
		self.baseData['Y1'] = pd.Series(Years1, index=self.baseData.index)
		self.baseData['Y2'] = pd.Series(Years2, index=self.baseData.index)
		self.baseData['Y3'] = pd.Series(Years3, index=self.baseData.index)
		self.baseData['Y4'] = pd.Series(Years4, index=self.baseData.index)
		self.baseData['Y5'] = pd.Series(Years5, index=self.baseData.index)
		self.baseData['commercial'] = pd.Series(commercial, index=self.baseData.index)
		self.baseData['residential'] = pd.Series(residential, index=self.baseData.index)
		self.baseData['office'] = pd.Series(office, index=self.baseData.index)
		self.baseData['retail'] = pd.Series(retail, index=self.baseData.index)
		self.baseData['garage'] = pd.Series(garage, index=self.baseData.index)
		self.baseData['storage'] = pd.Series(storage, index=self.baseData.index)
		self.baseData['factory'] = pd.Series(factory, index=self.baseData.index)
		self.baseData['other'] = pd.Series(other, index=self.baseData.index)

	def loadbin2bbl(self, binFile):
		with open(binFile, 'rb') as txtfile:
			stripped = (line.strip() for line in txtfile)
			lines = (line.split(",") for line in stripped if line)
			i = 0
			for line in lines:
				if i == 0:
					i += 1
					continue
				borough = line[0].strip("\"")
				block = line[1].strip("\"")
				lot = line[2].strip("\"")
				binNum = line[3].strip("\"")
				BBL = borough + block + lot
				try:
					assert(len(BBL) == 10)
				except AssertionError:
					print((borough, block, lot))
				if binNum not in self.bin2bbl:
					self.bin2bbl[binNum] = [BBL]
				else:
					#assert(self.bin2bbl[binNum] == BBL)
					if BBL in self.bin2bbl[binNum]:
						continue
					else:
						self.bin2bbl[binNum].append(BBL)
				self.bbl2bin[BBL] = binNum

	def loadbuilding2bin(self, buildingFile):
		with open(buildingFile, 'rb') as csvfile:
			i = 0
			lastLine = None
			currentDevelopment = None
			for line in csvfile:
				i += 1
				#if i < 3:
				#	continue
				IGNORE = ["NYCHA PROPERTY DIRECTORY", "DEVELOPMENT GUIDE"]
				spaces,ret = self.removeDupSpaces(line)
				stripped = ret.split(",")

				if len(stripped) == 0:
					lastLine = stripped
					continue
				if len(stripped) == 1 and stripped[0] not in IGNORE and spaces == 0:
					lastLine = stripped
					continue

				S2 = stripped[0].strip()
				if S2 == 'Managed by:' or S2 == '"Managed by:':
					if (len(lastLine) != 1 or (currentDevelopment is not None and lastLine[0].strip() == currentDevelopment)):
						lastLine = stripped
						continue
					currentDevelopment = lastLine[0].strip()
					lastLine = stripped
					continue
				elif S2 == 'Development (NY) #:' or S2 == '"Development (NY) #:':
					lastLine = stripped
					continue
				elif S2 == 'BLDG#' or S2 == 'BLDG# = Building #':
					lastLine = stripped
					continue
				buildingNumber = 0
				BIN = 0
				if len(stripped) > 2:
					#find which index has a 7 digit number
					if len(stripped[0]) == 7:
						lastLine = stripped
						continue
					if len(stripped[1]) == 7:
						try:
							BIN = int(stripped[1])
						except ValueError:
							lastLine = stripped
							continue
						try:
							buildingNumber = int(stripped[0])
						except ValueError:
							lastLine = stripped
							continue
					if len(stripped[2]) == 7:
						try:
							BIN = int(stripped[2])
						except ValueError:
							lastLine = stripped
							continue
						try:
							buildingNumber = int(stripped[0])
						except ValueError:
							try:
								buildingNumber = int(stripped[1])
							except ValueError:
								lastLine = stripped
								continue
				if buildingNumber == 0 or BIN == 0 or currentDevelopment is None:
					lastLine = stripped
					continue

				# if (currentDevelopment, buildingNumber) in self.building2bin:
				# 	try:
				# 		assert(self.building2bin[(currentDevelopment, buildingNumber)] == BIN)
				# 	except AssertionError:
				# 		print((self.building2bin[(currentDevelopment, buildingNumber)], BIN))
				# else:
				if currentDevelopment == '1162-1176 WASHINGTON AVENUE':
					currentDevelopment = 'WASHINGTON AVENUE'
				self.building2bin[(currentDevelopment, buildingNumber)] = str(BIN)
				lastLine = stripped

		# for (currentDevelopment, buildingNumber) in self.building2bin:
		# 	print(currentDevelopment + " building " + str(buildingNumber) + ": " + str(self.building2bin[(currentDevelopment,buildingNumber)]))
		# print(len(self.building2bin))






				#if i == 10:
				#	break
				

	def removeDupSpaces(self, line):
		newString = ""
		maxSpaces = 0
		i = 0
		j = 0
		while i < len(line):
			#case 1: if double space
			if j < len(line)-1 and line[j] == " " and line[j+1] == " ":
				while j < len(line) and line[j] == " ":
					j += 1
				#end of spaces, i = j
				maxSpaces = max(maxSpaces, j-i)
				i = j
				continue
			#case 2: regular characters
			while j < len(line):
				if j < len(line)-1 and line[j] == " " and line[j+1] == " ":
					break
				j += 1
			added = line[i:j]+"," if j != len(line) else line[i:]
			newString += added
			i = j
		newString = newString.strip()
		return (maxSpaces,newString)
			
		
		

NYCHAAnalysis()