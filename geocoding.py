from geocodio import GeocodioClient
import csv
import time

#uses Geocod.io for geocoding. 2500 queries per day limit.
#If you wish to run, uncomment the following line,
#but be careful or Peter will be homeless soon
runAPI = False
#runAPI = True

csvFile = "parking_garage_list.csv"

addressLists = []
with open(csvFile, 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	i = True
	for row in reader:
		if i:
			i = False
			continue
		else:
			addressNum = row[5]
			addressStreet1 = row[6]
			addressStreet2 = row[7]
			city = row[8]
			state = row[9]
			zipCode = row[10]
			extraSpace = ""
			if addressStreet2 != "":
				extraSpace = " "
			query = addressNum + " " + addressStreet1 + extraSpace + addressStreet2 + ", " + city + ", " + state + ", " + zipCode
			addressLists.append(query)
#print(addressLists)
print(len(addressLists))

client = None
if runAPI:
	client = GeocodioClient("a60b68a3bcaa9a0b368a6660098b5aa35855906")

latlonFile = "parkingGarageFile1.csv"
with open(latlonFile, 'wb') as csvfile:
	latlonwriter = csv.writer(csvfile, delimiter=',')
	i = 0
	for address in addressLists:
		if i < 650:
			i += 1
			continue
		if i % 100 == 0:
			print("\n\n" + "Completed " + str(i) + " queries\n\n")
		i += 1
		geocoded_location = None
		if runAPI:
			geocoded_location = client.geocode(address)
		if geocoded_location is None:
			continue
		coords = geocoded_location.coords
		if coords is None:
			continue
		print(coords)
		latlonwriter.writerow([address,coords[0],coords[1]])

#client = GeocodioClient("a60b68a3bcaa9a0b368a6660098b5aa35855906")
#for address in addressLists:
#	geocoded_location = client.geocode(address)
