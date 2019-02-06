import web
import os
import dynamicPopulation
import time
#from dynamicPopulation import showDynamicPopulation
import CarCounting.getDOTstream as D
import graphBackend
import staticData.foursquareCheckinData as FS
import staticData.staticTaxiData as TD
import staticData.staticCensusData as CD
#from streamDaemon import streams
import streamDaemon
import dynamicData.subwayData as SD




#Stream = streamDaemon.S
print("Assigned stream")
urls = (
	#"/(.*)", 'Service',
#	"/realtime", dynamicPopulation.doPopulation,
	"/camera", D.DOTstream,
	"/foursquareData", FS.foursquareData,
	"/taxiData", TD.taxiData,
	"/censusData", CD.censusData,
	"/graph", graphBackend.G,
	"/subway", SD.subwayData,
	"/", "baseURL"
	)



#initialization = dynamicPopulation.showDynamicPopulation()
#initialization.startup()

class baseURL:
	def GET(self):
		return "200 OK"
	def POST(self):
		return "200 OK"

class Service:
	def GET(self, name):
		web.header('Access-Control-Allow-Origin',      '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		return {'message': 'GET OK!'}
	def POST(self, name):
		web.header('Access-Control-Allow-Origin',      '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		data = web.data()
		return {'message': "POST OK! %s" % data}

class MyApplication(web.application):
	def run(self, port=8080, *middleware):
		#self.runDynamicPopulation()
		#self.runTrafficCount()
		func = self.wsgifunc(*middleware)
		return web.httpserver.runsimple(func, ('0.0.0.0', port))

	#def runTrafficCount(self):


	def runDynamicPopulation(self):
		#run1 = dynamicPopulation.showDynamicPopulation(1)
		while True:
			print("\n\nRunning dynamic\n\n")
			#run1.getBlocks2Occupancy(20)
			#run1.startup()
			#run1.plotBuildings()
			#run1.plotRealtime()
			time.sleep(30)


		return

def notfound():
	return web.notfound("404 not found")

def run():
	app = MyApplication(urls, globals())
	app.notfound = notfound
	app.run(port=8001)