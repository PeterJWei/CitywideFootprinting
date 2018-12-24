import csv
from datetime import datetime
from pytz import timezone
tz = timezone('US/Eastern')
data = []
with open ('dataset_tsmc2014/dataset_TSMC2014_NYC.txt', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter='\t')
	i = 0
	for row in reader:
		
		lat = row[4]
		lon = row[5]
		t = row[7]
		datetime_object = datetime.strptime(t, '%a %b %d %H:%M:%S +0000 %Y')
		h = datetime_object.hour
		m = datetime_object.minute
		data.append((lat, lon, (h - 5)%24, m))
		if i % 1000 == 0:
			print(str(i*100.0/227428) + "%...")
			print(datetime_object)
		i+= 1

		#Tue Apr 03 18:00:09 +0000 2012

file = "venueLocations.csv"
with open(file, 'wb') as csvfile:
	i = 0
	csvwriter = csv.writer(csvfile, delimiter=',')
	csvwriter.writerow(["latitude", "longitude", "hour", "minute"])
	for datum in data:
		if i % 1000 == 0:
			print(str(i*100.0/227428) + "%...")
		(lat, lon, h, m) = datum
		csvwriter.writerow([lat, lon, h, m])
		i += 1