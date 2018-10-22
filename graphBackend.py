
from subwayStream import subwayStream
import web
import json


urls = ("/", "graphTraffic")

class graphTraffic:
	def GET(self):
		MTAstream = subwayStream()
		#stationTrains = MTAstream.getData(0x1FF)
		T1 = 0
		# if '116' in stationTrains:
		# 	T1 = stationTrains['116']
		T2 = 0
		# if '117' in stationTrains:
		# 	T2 = stationTrains['117']
		
		j = [{
				"id":"n9",
				"traffic":T1
			},
			{
				"id":"n8",
				"traffic":T2
			}]
		return json.dumps(j)

G = web.application(urls, locals());