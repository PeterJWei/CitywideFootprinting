import csv
import pickle

class loadTaxiRoutes:
	def __init__(self):
		self.StartLocations = []
		self.EndLocations = []
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
					if pickup_long is None or pickup_lat is None:
						raise Exception("Pickup Coordinates are Missing")
					if dropoff_long is None or dropoff_lat is None:
						raise Exception("Dropoff Coordinates are Missing")
					continue
				self.StartLocations.append((line[pickup_lat], line[pickup_long]))
				self.EndLocations.append((line[dropoff_lat], line[dropoff_long]))
			print(len(self.StartLocations))
			print(len(self.D["start"]))
			print(len(self.D["end"]))
			self.save_obj(self.D, fileName)

	def save_obj(self, obj, name):
		with open('pklObjects/'+ name + '.pkl', 'wb') as f:
			pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

	def load_obj(self, name):
		with open('pklObjects/' + name + '.pkl', 'rb') as f:
			return pickle.load(f)

L = loadTaxiRoutes()
L.loadRoutes("output_1_1")