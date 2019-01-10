import csv
from datetime import datetime

class loadCuebiq:
	def __init__(self):
		self.times = []

	def loadRoutes(self, fileName):
		csvFile = fileName + ".csv"
		with open(csvFile, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter='\t')
			for line in reader:
				timestamp = int(line[0])
				d = datetime.utcfromtimestamp(timestamp)
				#print((d.hour, d.minute))
				#return
				lat = float(line[3])
				lon = float(line[4])
				self.times.append((lat, lon, d.hour, d.minute))
	def saveRoutes(self, saveFile):
		file = saveFile
		with open(file, 'wb') as csvfile:
			csvwriter = csv.writer(csvfile, delimiter=',')
			csvwriter.writerow(["latitude", "longitude", "hour", "minute"])
			for i in range(len(self.times)):
				csvwriter.writerow(list(self.times[i]))
		
L = loadCuebiq()
L.loadRoutes("part-00000")
L.saveRoutes("testTimes.csv")