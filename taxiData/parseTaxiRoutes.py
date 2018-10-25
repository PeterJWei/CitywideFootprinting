import csv
import pickle
from datetime import datetime

class loadTaxiRoutes:
	def __init__(self):
		self.StartLocations = []
		self.EndLocations = []
		self.PickupTime = []
		self.DropoffTime = []
		self.D = {}
		self.D["start"] = self.StartLocations
		self.D["end"] = self.EndLocations

	def loadRoutes(self, fileName):
		csvFile = "csvFiles/" + fileName + ".csv"
		with open(csvFile, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			pickup_long = None
			pickup_lat = None
			dropoff_long = None
			dropoff_lat = None
			pickup_time = None
			dropoff_time = None
			first = True
			for line in reader:
				if first:
					first = False
					print(line)
					for i in range(len(line)):
						key = line[i]
						if key == "pickup_longitude" and pickup_long is None:
							pickup_long = i
						elif key == "pickup_latitude" and pickup_lat is None:
							pickup_lat = i
						elif key == "dropoff_longitude" and dropoff_long is None:
							dropoff_long = i
						elif key == "dropoff_latitude" and dropoff_lat is None:
							dropoff_lat = i
						elif key == "pickup_datetime" and pickup_time is None:
							pickup_time = i
						elif key == "dropoff_datetime" and dropoff_time is None:
							dropoff_time = i
					if pickup_long is None or pickup_lat is None:
						raise Exception("Pickup Coordinates are Missing")
					if dropoff_long is None or dropoff_lat is None:
						raise Exception("Dropoff Coordinates are Missing")
					if pickup_time is None or dropoff_time is None:
						raise Exception("Times are missing")
					continue

				self.StartLocations.append((line[pickup_lat], line[pickup_long]))
				self.EndLocations.append((line[dropoff_lat], line[dropoff_long]))
				#2013-01-01 15:11:48
				P = line[pickup_time]
				datetime_object = datetime.strptime(P, '%Y-%m-%d %H:%M:%S')
				self.PickupTime.append(datetime_object.hour)
				D = line[dropoff_time]
				datetime_object = datetime.strptime(D, '%Y-%m-%d %H:%M:%S')
				self.DropoffTime.append(datetime_object.hour)
			self.save_obj(self.D, fileName)

	def saveRoutes(self):
		file = "startLocations.csv"
		with open(file, 'wb') as csvfile:
			csvwriter = csv.writer(csvfile, delimiter=',')
			csvwriter.writerow(["latitude", "longitude", "time"])
			for i in range(len(self.StartLocations)):
				row = self.StartLocations[i]
				(lat, lon) = row
				csvwriter.writerow([lat, lon, self.PickupTime[i]])
		file = "endLocations.csv"
		with open(file, 'wb') as csvfile:
			csvwriter = csv.writer(csvfile, delimiter=',')
			csvwriter.writerow(["latitude", "longitude", "time"])
			for i in range(len(self.EndLocations)):
				row = self.EndLocations[i]
				(lat, lon) = row
				csvwriter.writerow([lat, lon, self.DropoffTime[i]])

	def save_obj(self, obj, name):
		with open('pklObjects/'+ name + '.pkl', 'wb') as f:
			pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

	def load_obj(self, name):
		with open('pklObjects/' + name + '.pkl', 'rb') as f:
			return pickle.load(f)

L = loadTaxiRoutes()
L.loadRoutes("output_1_1")
