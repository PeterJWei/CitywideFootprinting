from pytz import timezone
from google.transit import gtfs_realtime_pb2
import urllib
import datetime
import csv

from collections import OrderedDict
# Storing trip related data
# Note : some trips wont have vehicle data

class tripupdate(object):
	def __init__(self):
		self.tripId = None
		self.routeId = None
		self.startDate = None
		self.direction = None
		self.vehicleData = None
		self.nextStop = None # Format {stopId : [arrivalTime,departureTime]}
		self.nextStopTimes = None

	def __str__(self):
		start = ""
		if self.tripId is None or self.routeId is None or self.direction is None:
			return "None"
		else:
			start = "trip ID: " + str(self.tripId) + ", routeId: " + str(self.routeId) + "\n"
		stopStr = ""
		for stop in self.futureStops:
			stopStr += stop + ", " + str(self.futureStops[stop]) + "\n"
		return stopStr + start

class subwayStream:
	def __init__(self):
		self.stationDefinitions("SubwayStations/stops.csv")
		self.TIMEZONE = timezone('America/New_York')
		self.KEY = '914716d7b50514f729f51936174bc790'
		self.lastStops = {}
		return

	def stationDefinitions(self, stationFile):
		self.stopID2parent = {}
		with open (stationFile, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = True
			for row in reader: 
				if i: #skip the first line
					i = False
					continue
				else:
					stationName = row[0]
					parent = row[-1]
					if parent == "":
						parent = stationName
					self.stopID2parent[stationName] = parent

	def getData(self):
		stationTrains = {}
		feed = gtfs_realtime_pb2.FeedMessage()
		url = 'http://datamine.mta.info/mta_esi.php?key=' + self.KEY + '&feed_id=1'
		response = urllib.urlopen(url)
		feed.ParseFromString(response.read())
		#for entity in feed.entity:
		#	if entity.HasField('trip_update'):
		#		print(entity.trip_update)

		timestamp = feed.header.timestamp
		print("Timestamp: " + str(timestamp))
		nytime = datetime.datetime.fromtimestamp(timestamp, self.TIMEZONE)
		print("NYC Time: " + str(nytime))

		self.timestamp = timestamp
		self.tripUpdates = []

		for entity in feed.entity:
			# Trip update represents a change in timetable
			if entity.trip_update and entity.trip_update.trip.trip_id:
				# Assign the tripupdate fields
				t = tripupdate()
				t.tripId = entity.trip_update.trip.trip_id
				t.routeId = entity.trip_update.trip.route_id
				t.startDate = entity.trip_update.trip.start_date
				t.direction = entity.trip_update.trip.direction_id

				# There can be many StopTimeUpdate messages
				for st_update in entity.trip_update.stop_time_update:
					t.nextStop = st_update.stop_id
					t.nextStopTimes = (st_update.arrival.time, st_update.departure.time)
					# times = []
					# times.append({"arrivalTime": st_update.arrival.time})
					# times.append({"departureTime": st_update.departure.time})
					# t.futureStops[st_update.stop_id] = times
					break
				self.tripUpdates.append(t)
		for t in self.tripUpdates:
			if t.tripId not in self.lastStops: #new train
				self.lastStops[t.tripId] = t.nextStop
				continue
			else:
				nextStation = t.nextStop
				leftStation = self.lastStops[t.tripId]
				if leftStation != nextStation: #train has left the station
					#print((t, leftStation, nextStation))
					if leftStation not in stationTrains:
						stationTrains[self.stopID2parent[leftStation]] = 0
					stationTrains[self.stopID2parent[leftStation]] += 1 # another train has gone through the station
					self.lastStops[t.tripId] = nextStation #train is now going to the next station
		removeTrains = []
		for t in self.lastStops:
			found = False
			for t_u in self.tripUpdates:
				if t_u.tripId == t:
					found = True
					break
			if not found:
			#if t not in self.tripUpdates: # train has finished
				lastStation = self.lastStops[t]
				#print(t)
				if lastStation not in stationTrains:
					stationTrains[self.stopID2parent[lastStation]] = 0
				stationTrains[self.stopID2parent[lastStation]] += 1
				removeTrains.append(t)
		for t in removeTrains:
			self.lastStops.pop(t, None) # remove the train

		return stationTrains

#S = subwayStream()
#S.getData()