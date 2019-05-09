import web
import energyServer
import datetime
urls = ("/", "personalFootprint"
		)


class personalFootprint:
	def GET(self):
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		start = datetime.datetime(2019, 5, 9, 0)
		end = datetime.datetime.now()
		ret = energyServer.db.retrieveStateParameters(start, end)
		footprint = ret["footprint"]
		jsonDump = json.dumps(footprint)
		return jsonDump

footprint = web.application(urls, locals());