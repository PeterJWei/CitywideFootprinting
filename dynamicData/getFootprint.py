import web
import energyServer
import datetime
import calendar
import json
urls = ("/", "personalFootprint"
		)


class personalFootprint:
	def GET(self):
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true') 
		start = calendar.timegm(datetime.datetime(2019, 5, 9, 0).utctimetuple())
		end = calendar.timegm(datetime.datetime.now().utctimetuple())
		ret = energyServer.db.retrieveStateParameters(start, end)
		#footprint = ret["footprint"]

		jsonDump = json.dumps(ret)
		return jsonDump

footprint = web.application(urls, locals());