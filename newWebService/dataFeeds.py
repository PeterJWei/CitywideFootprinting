from google.transit import gtfs_realtime_pb2
import urllib

class dataFeeds:
	def __init__(self):
		self.MTA_KEY = "914716d7b50514f729f51936174bc790"
		self.BUS_KEY = "9e48e333-1db4-4ea6-a0f5-674fc00edb77"
		#self.getSubwayFeeds()
		self.getLIRRFeed()
		self.getMetroNorthFeed()


	def getSubwayFeeds(self):
		for feed_id in [1, 2, 11, 16, 21, 26, 31, 36, 51]:
			#feed_id = 1: 1, 2, 3, 4, 5, 6, S lines
			#feed_id = 2: L line
			#feed_id = 11: SIR staten island railway
			#feed_id = 16: N, Q, R, W lines
			#feed_id = 21: B, D, F, M lines
			#feed_id = 26: A, C, E, H, S (Franklin Avenue Shuttle) lines
			#feed_id = 31: G line
			#feed_id = 36: J, Z lines
			#feed_id = 51: 7 line
			feed = gtfs_realtime_pb2.FeedMessage()
			response = urllib.urlopen('http://datamine.mta.info/mta_esi.php?key=%s&feed_id=%d' % (self.MTA_KEY, feed_id))
			feed.ParseFromString(response.read())
			for entity in feed.entity:
				if entity.HasField(''):

			print feed

	def getLIRRFeed(self):
		feed = gtfs_realtime_pb2.FeedMessage()
		response = urllib.urlopen('https://mnorth.prod.acquia-sites.com/wse/LIRR/gtfsrt/realtime/%s/json' % self.MTA_KEY)
		readResponse = response.read()
		print(readResponse)
		feed.ParseFromString(readResponse)
		print feed

	def getMetroNorthFeed(self):
		feed = gtfs_realtime_pb2.FeedMessage()
		response = urllib.urlopen('https://mnorth.prod.acquia-sites.com/wse/gtfsrtwebapi/v1/gtfsrt/%s/getfeed' % self.MTA_KEY)
		feed.ParseFromString(response.read())
		print feed

	def getBusTimes(self):
		feed = gtfs_realtime_pb2.FeedMessage()
		response = urllib.urlopen('http://gtfsrt.prod.obanyc.com/vehiclePositions?key=%s' % self.BUS_KEY)
		feed.ParseFromString(response.read())
		print feed
#Train Feeds

#Subway Feeds

#Bus Feeds

#Traffic Feeds

#Ferry Feeds