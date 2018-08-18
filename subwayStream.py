from google.transit import gtfs_realtime_pb2
import urllib

class subwayStream:
	def __init__(self):
		self.KEY = '914716d7b50514f729f51936174bc790'
		return

	def getData(self):
		feed = gtfs_realtime_pb2.FeedMessage()
		url = 'http://datamine.mta.info/mta_esi.php?key=' + self.KEY + '&feed_id=1'
		response = urllib.urlopen(url)
		feed.ParseFromString(response.read())
		for entity in feed.entity:
			if entity.HasField('trip_update'):
				print(entity.trip_update)

S = subwayStream()
S.getData()