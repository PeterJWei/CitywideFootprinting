import csv
import web
import json
import datetime
import energyServer


urls = ("/subwayData", "subway",
		"/subwayTotal", "subwayTotal",
		"/subwayChanges", "subwayChanges",
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
		energyServer.S.clearList()
		return jsonDump

class subwayTotal:
	def GET(self):
		B = energyServer.S.totalChangesList
		jsonDump = json.dumps(B)
		return jsonDump

class subwayChanges:
	def GET(self):
		data = web.input()
		BBL = data.BBL
		populationDifference = energyServer.S.totalChanges[BBL]
		return json.dumps(populationDifference)

subwayData = web.application(urls, locals());