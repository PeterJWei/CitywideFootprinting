import csv
import web
import json
import datetime
import energyServer


urls = ("/subwayData", "subway",
	"/", "check")


class check:
	def GET(self):
		return "200 OK"

def getTime():
	web.header('Access-Control-Allow-Origin', '*')
	web.header('Access-Control-Allow-Credentials', 'true')
	now = datetime.datetime.now()
	hour = now.hour
	minute = now.minute
	return (hour, minute)

class subway:
	def GET(self):
		hour, minute = getTime()
		B = energyServer.S.buildingChangesList
		jsonDump = json.dumps(B)
		energyServer.Stream.clearList()
		return jsonDump

subwayData = web.application(urls, locals());