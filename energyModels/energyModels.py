import csv
import time
import numpy as np
import pandas as pd
import math
from utils.LL84Dictionaries import propertyDictionary as pDict
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

class modelAnalysis:
	def __init__(self):
		self.file = "../LL84NYCBuildings.csv"
		self.baseData = None
		self.OLSData = None
		self.target = None
		#self.viewHeader()
		self.loadData()
		#self.transferData()
		self.OLS()
		#self.statistics()
	
	def viewHeader(self):
		with open(self.file, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for row in reader:
				i = 0
				for column in row:
					print(str(i) + " :" + column)
					i += 1
				break

	def loadData(self):
		BBLs = []
		Boroughs = []
		GrossFloorArea = []
		PropertyTypes = []
		LargestPropertyType = []
		LargestFloorArea = []
		SecondPropertyType = []
		SecondFloorArea = []
		ThirdPropertyType = []
		ThirdFloorArea = []
		YearBuilt = []
		Occupancy = []
		WeatherNormalizedIntensity = []
		WeatherNormalized = []
		PropResidential = []
		PropOffice = []
		PropRetail = []
		PropStorage = []
		PropFactory = []
		Manhattan = []
		Brooklyn = []
		Queens = []
		Bronx = []
		StatenIsland = []
		Years1 = []
		Years2 = []
		Years3 = []
		Years4 = []
		Years5 = []
		typeDictionary = {'Residential':0, 'Office':1, 'Retail':2, 'Storage':3, 'Factory':4}
		boroughDictionary = {'':0, 'Manhattan':1, 'Brooklyn':2, 'Queens':3, 'Bronx':4, 'Staten Island':5}
		with open(self.file, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = True
			for row in reader:
				if i:
					i = not i
					continue

				if row[14] == '':
					continue
				if row[23] == 'Not Available' or row[31] == 'Not Available' or float(row[31]) < 1.0 or float(row[43]) < 1.0:
					continue

				BBLs.append(row[5])
				Boroughs.append(row[13])

				b = [0, 0, 0, 0, 0, 0]
				b[boroughDictionary[row[13]]] = 1
				Manhattan.append(b[1])
				Brooklyn.append(b[2])
				Queens.append(b[3])
				Bronx.append(b[4])
				StatenIsland.append(b[5])
				#GrossFloorArea.append(float(row[14]))
				GrossFloorArea.append(math.log(float(row[14])))
				PropertyTypes.append(row[16])


				LargestPropertyType.append(row[17])
				val1 = row[18] if row[18] != "Not Available" else 0
				val2 = row[20] if row[20] != "Not Available" else 0
				val3 = row[22] if row[22] != "Not Available" else 0
				LargestFloorArea.append(val1)
				SecondPropertyType.append(row[19])
				SecondFloorArea.append(val2)
				ThirdPropertyType.append(row[21])
				ThirdFloorArea.append(val3)


				GFA = float(row[14])
				proportions = [0.0, 0.0, 0.0, 0.0, 0.0]
				type1 = pDict[row[17]]
				type2 = pDict[row[19]]
				type3 = pDict[row[21]]
				proportions[typeDictionary[type1]] = float(val1)/GFA
				proportions[typeDictionary[type2]] = float(val2)/GFA
				proportions[typeDictionary[type3]] = float(val3)/GFA

				PropResidential.append(proportions[0])
				PropOffice.append(proportions[1])
				PropRetail.append(proportions[2])
				PropStorage.append(proportions[3])
				PropFactory.append(proportions[4])

				YearBuilt.append(int(row[23]))
				
				YB = [0, 0, 0, 0, 0]
				if row[23] <= 1930:
					YB[0] = 1
				elif row[23] > 1930 and row[23] <= 1950:
					YB[1] = 1
				elif row[23] > 1950 and row[23] <= 1970:
					YB[2] = 1
				elif row[23] > 1970 and row[23] <= 1990:
					YB[3] = 1
				elif row[23] > 1990:
					YB[4] = 1
				Years1.append(YB[0])
				Years2.append(YB[1])
				Years3.append(YB[2])
				Years4.append(YB[3])
				Years5.append(YB[4])
				Occupancy.append(int(row[25]))
				WeatherNormalizedIntensity.append(math.log(float(row[31])))
				WeatherNormalized.append(math.log(float(row[43])))
				#WeatherNormalized.append(float(row[43]))
		self.baseData = pd.DataFrame({
			'BBL':BBLs,
			'Borough':Boroughs,
			'GrossFloorArea':GrossFloorArea,
			'PropertyTypes':PropertyTypes,
			'LargestPropertyType':LargestPropertyType,
			'LargestFloorArea':LargestFloorArea,
			'SecondPropertyType':SecondPropertyType,
			'SecondFloorArea':SecondFloorArea,
			'ThirdPropertyType':ThirdPropertyType,
			'ThirdFloorArea':ThirdFloorArea,
			'YearBuilt':YearBuilt,
			'Occupancy':Occupancy,
			'WeatherNormalizedIntensity':WeatherNormalizedIntensity,
			'WeatherNormalized':WeatherNormalized
			})
		self.OLSData = pd.DataFrame({
			'GrossFloorArea':GrossFloorArea,
			'Y1':Years1,
			'Y2':Years2,
			'Y3':Years3,
			'Y4':Years4,
			'Y5':Years5,
			'YearBuilt':YearBuilt,
			'MN':Manhattan,
			'BR':Brooklyn,
			'QN':Queens,
			'SI':StatenIsland,
			'BX':Bronx,
			'Residential':PropResidential,
			'Office':PropOffice,
			'Retail':PropRetail,
			'Storage':PropStorage,
			'Factory':PropFactory
			})
		self.target = pd.DataFrame({
			'EUI':WeatherNormalized#Intensity
			})

	def transferData(self):
		#{'LargestPropertyType':self.baseData['LargestPropertyType']})
		for i in range(len(self.baseData['LargestPropertyType'])):
			self.baseData['LargestPropertyType'][i] = pDict[self.baseData['LargestPropertyType'][i]]
			self.baseData['SecondPropertyType'][i] = pDict[self.baseData['SecondPropertyType'][i]]
			self.baseData['ThirdPropertyType'][i] = pDict[self.baseData['ThirdPropertyType'][i]]
		#self.OLSData = pd.concat([self.OLSData, self.baseData['LargestPropertyType']], axis=1)

	def OLS(self):
		X_train, X_test, y_train, y_test = train_test_split(self.OLSData, self.target, test_size=0.33, random_state=42)
		#X = self.OLSData
		#y = self.target
		lm = linear_model.LinearRegression()
		model = lm.fit(X_train,y_train)
		#score = lm.score(X,y)
		predictions = lm.predict(X_test)
		print("Total samples: " + str(len(self.OLSData)))
		print("Number of test samples: " + str(len(y_test)))
		print("Mean Absolute Error: %.2f" % mean_absolute_error(y_test, predictions))
		print("Mean Squared Error: %.2f" % mean_squared_error(y_test, predictions))
		print("Variance Score: %.2f" % r2_score(y_test, predictions))

	def statistics(self):
		#print(self.baseData.head())
		print(self.OLSData.describe())

M = modelAnalysis()